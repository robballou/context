import json
import os
import sys
import importlib

from commands import Observable, Event

class Contexts(Observable):
    """
    Global contexts class
    """

    #
    # METHODS
    #
    def __init__(self, data=None, **kwargs):
        super(Contexts, self).__init__()

        # the contexts configuration data
        self.contexts = {}

        # the key of the current context
        self.current_context = None

        # commands that have been processed and are ready to run
        self.registered_commands = {}

        # stores a map of aliases to commands
        self.command_aliases = {}

        # holds the commands configured in the user's .contexts file
        self.configured_commands = None

        # plugins
        self.plugins = []
        self.loaded_plugins = {}

        # settings management
        defaults = {
            "context_file": "~/.contexts",
            "data_file": "~/.contexts_data"
        }

        defaults = dict(defaults.items() + kwargs.items())
        for default in defaults:
            try:
                setattr(self, default, defaults[default])
            except AttributeError:
                pass

        if data:
            self.parse(data)

        # load commands
        commands = [
            "context.commands.contrib.bundler",
            "context.commands.contrib.clear",
            "context.commands.contrib.contexts",
            "context.commands.contrib.current",
            "context.commands.contrib.django",
            "context.commands.contrib.edit",
            "context.commands.contrib.git",
            "context.commands.contrib.gulp",
            "context.commands.contrib.links",
            "context.commands.contrib.npm",
            "context.commands.contrib.switch",
            "context.commands.contrib.vagrant",
            "context.commands.contrib.web",
            "context.commands.contrib.www",
        ]

        if self.configured_commands:
            commands = commands + self.configured_commands

        for command in commands:
            command_name = command.split(".")[-1]
            class_name = command_name.title()

            try:
                module = importlib.import_module(command)
                this_command = getattr(module, class_name)
                self.registered_commands[command_name] = this_command

                # try to register any aliases
                try:
                    self.command_aliases[this_command.alias] = command_name
                except AttributeError:
                    pass
            except ImportError, e:
                sys.stderr.write("Could not find command module: %s (%s)\n" % (command, e))
                sys.exit(1)

        # load the switchers' data file
        contexts_data_file = self.get_contexts_data_file()
        if os.path.exists(contexts_data_file):
            contexts_data = json.loads(open(contexts_data_file, 'r').read())
            if 'current_context' in contexts_data:
                self.current_context = contexts_data['current_context']

    def get(self, context=None):
        """Get a specific context"""
        if not context:
            raise Exception('test')
            sys.stderr.write("Cannot get context\n")
            sys.exit(1)

        # contexts can't start with "_"
        if context.startswith('_'):
            return False

        if not context and self.current_context:
            return self.contexts[self.current_context]

        if context in self.contexts:
            return self.contexts[context]
        return False

    def get_contexts_data_file(self):
        """Return the path for the data file"""
        return os.path.expanduser(self.data_file)

    def help(self):
        """
        Display some usage and command information
        """
        sys.stderr.write("Usage: context [command] [subcommand ...]\n\n")
        sys.stderr.write("Commands:\n")

        # show registered commands
        commands = self.registered_commands.keys()
        commands.sort()
        for command in commands:
            this_command = command
            try:
                this_command = "%s (%s)" % (this_command, self.registered_commands[command].alias)
            except AttributeError:
                pass
            sys.stderr.write("\t%s\n" % this_command)

    def initialize_plugins(self):
        for plugin in self.plugins:
            try:
                plugin_name = plugin.split(".")[-1]
                plugin_name = plugin_name.replace("_", " ")
                plugin_class_name = plugin_name.title().replace(" ", "")

                module = importlib.import_module(plugin)
                this_plugin = getattr(module, plugin_class_name)
                self.loaded_plugins[plugin] = this_plugin(self)
            except Exception, e:
                sys.stderr.write("Could not import plugin: %s\n\t%s\n" % (plugin, e))
                raise e

    def parse(self, data):
        """
        Parse/load the contexts data
        """
        try:
            self.contexts = json.loads(data)
        except Exception, e:
            sys.stderr.write("Error: Could not load contexts: %s\n" % e)
            sys.exit(1)

        for context in self.contexts:
            if context == '__commands':
                self.configured_commands = self.contexts[context]
            elif context == '__plugins':
                self.plugins = self.contexts[context]
                self.initialize_plugins()

    def run_command(self, command, args):
        """
        Run the specified command
        """
        # check if the command is registered
        if command in self.registered_commands:
            this_command = self.registered_commands[command]
        # check if this is an alias of a registered command
        elif command in self.command_aliases:
            command = self.command_aliases[command]
            this_command = self.registered_commands[command]
        else:
            sys.stderr.write("Invalid command: %s\n" % command)
            sys.exit(1)

        # run the command
        command_object = this_command()

        # check if there is a current context before calling get()
        context = None
        if self.current_context:
            context = self.get(self.current_context)

        # actually run the command
        pre_event = Event(self, current_context=context, command_args=args)
        self.trigger("%s.pre" % command, pre_event)
        command_object.run(context, args, self)

        if self.current_context:
            context = self.get(self.current_context)
        post_event = Event(self, current_context=context, command_args=args)
        self.trigger(command, post_event)

    def switch(self, context):
        """
        Switch contexts to the provided context key
        """

        new_context = self.get(context)
        if not new_context:
            raise Exception('Invalid context: %s' % context)

        self.current_context = context
        fp = open(self.get_contexts_data_file(), 'w')
        data = json.dumps({'current_context': self.current_context})
        fp.write(data)
        fp.close()
