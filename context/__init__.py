import json
import os
import sys
import importlib
import re

from commands import Observable, Event

class InvalidContextException(Exception):
    pass

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

        self.variable_pattern = re.compile(r'\$([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)')

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

        # default commands to load
        commands = [
            "context.commands.contrib.bash",
            "context.commands.contrib.bundler",
            "context.commands.contrib.clear",
            "context.commands.contrib.contexts",
            "context.commands.contrib.current",
            "context.commands.contrib.django",
            "context.commands.contrib.docker",
            "context.commands.contrib.drush",
            "context.commands.contrib.edit",
            "context.commands.contrib.git",
            "context.commands.contrib.gulp",
            "context.commands.contrib.links",
            "context.commands.contrib.npm",
            "context.commands.contrib.shell",
            "context.commands.contrib.switch",
            "context.commands.contrib.ssh",
            "context.commands.contrib.vagrant",
            "context.commands.contrib.web",
            "context.commands.contrib.www",
            "context.commands.contrib.z",
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
        if os.path.exists(contexts_data_file) and os.path.isfile(contexts_data_file):
            contexts_data = json.loads(open(contexts_data_file, 'r').read())
            if 'current_context' in contexts_data:
                self.current_context = contexts_data['current_context']

    def file_exists(self, filename, context):
        path = os.path.expanduser(os.path.join(context['git'], filename))
        return os.path.exists(path)

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

    def message(self, message):
        sys.stderr.write("%s\n" % message)

    def parse(self, data):
        """
        Parse/load the contexts data
        """
        try:
            self.contexts = self.parse_contexts(json.loads(data))
        except TypeError, te:
            self.contexts = {}
            for contexts_item in data:
                contexts_data = self.parse_contexts(json.loads(contexts_item))
                for data_key, data_item in contexts_data.iteritems():
                    if data_key not in self.contexts:
                        self.contexts[data_key] = data_item
                    else:
                        try:
                            self.contexts[data_key].update(data_item)
                        except Exception, e:
                            self.contexts[data_key].extend(data_item)

        except Exception, e:
            sys.stderr.write("Error: Could not load contexts: %s\n" % e)
            sys.exit(1)

        for context in self.contexts:
            if context == '__commands':
                self.configured_commands = self.contexts[context]
            elif context == '__plugins':
                self.plugins = self.contexts[context]
                self.initialize_plugins()

    def parse_contexts(self, contexts):
        """Parse the loaded contexts for variables"""

        # loop through the contexts
        for context in contexts:
            # skip controls (items that start with __)
            if context.startswith('__'):
                continue

            # loop through the items within the context
            for setting in contexts[context]:
                this_setting = contexts[context][setting]
                # parse the string
                if isinstance(this_setting, basestring):
                    this_setting = self.parse_variables(this_setting, contexts[context])
                else:
                    for subsetting in this_setting:
                        # lists don't like this
                        try:
                            this_subsetting = this_setting[subsetting]
                            if isinstance(this_subsetting, basestring):
                                this_subsetting = self.parse_variables(this_subsetting, contexts[context])
                            this_setting[subsetting] = this_subsetting
                        except TypeError:
                            pass
                contexts[context][setting] = this_setting
        return contexts

    def parse_variables(self, setting_string, context):
        """Parse the string for variables and replace with values from the context"""

        match = self.variable_pattern.search(setting_string)
        if match:
            # we need to parse variables
            for variable in match.groups():
                if variable in context:
                    setting_string = setting_string.replace("$%s" % variable, context[variable])
        return setting_string

    def run_command(self, command, args, remaining_args=None):
        """
        Run the specified command
        """

        try:
            command_args = None
            try:
                command, command_args = command.split(':')
                command_args.trim()
            except Exception, e:
                pass

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

            # check if there is a current context before calling get()
            context = None
            if self.current_context:
                context = self.get(self.current_context)
            try:
                if args.context:
                    context = self.get(args.context)
            except AttributeError, e:
                pass

            if not context:
                raise Exception('Invalid context')

            # run the command
            command_object = this_command(
                command,
                context,
                self,
                command_args,
                remaining_args
            )

            # catch cases where the switch is to an invalid context
            if command == 'switch':
                new_context = self.get(args.subcommand[0])
                if not new_context:
                    raise InvalidContextException('Invalid context: %s' % args.subcommand[0])

            # actually run the command
            pre_event = Event(self, current_context=context, command_args=args)
            self.trigger("%s.pre" % command, pre_event)
            command_object.run(context, args, self)

            if self.current_context:
                context = self.get(self.current_context)
            post_event = Event(self, current_context=context, command_args=args)
            self.trigger(command, post_event)
        except InvalidContextException, e:
            self.message("%s" % e)
            sys.exit(1)

    def switch(self, context):
        """
        Switch contexts to the provided context key
        """
        new_context = self.get(context)
        if not new_context:
            raise InvalidContextException('Invalid context: %s' % context)

        self.current_context = context
        fp = open(self.get_contexts_data_file(), 'w')
        data = json.dumps({'current_context': self.current_context})
        fp.write(data)
        fp.close()
