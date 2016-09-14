import os
import sys


class Event(object):
    """
    Event object used when triggering events
    """
    def __init__(self, context, **kwargs):
        self.context = context
        self.attributes = {}
        for kwarg in kwargs:
            self.attributes[kwarg] = kwargs[kwarg]


class Observable(object):
    """
    Base observerable class

    Allow classes to subscribe and trigger events.
    """
    def __init__(self):
        self.callbacks = {}

    def subscribe(self, event, callback):
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)

    def trigger(self, trigger, *args):
        if trigger in self.callbacks:
            for callback in self.callbacks[trigger]:
                callback(*args)


class Command(object):
    """Base Command class"""

    def __init__(self, command, context, contexts, command_args=None, remaining_args=None):
        super(Command, self).__init__()

        self.command = command
        self.context = context
        self.contexts = contexts
        self.command_args = command_args
        self.remaining_args = remaining_args
        self.settings = {}
        self.environment = {}
        self.ssh = None

        # set self.settings to the command settings, if available
        try:
            self.settings = context['settings'][command]
        except Exception, e:
            pass

    def default(self, context, args, contexts):
        pass

    def error_message(self, message):
        sys.stderr.write("%s\n" % message)

    def get_options(self):
        """Add options to this command"""
        options = ""

        try:
            for option in self.remaining_args:
                options = "%s %s" % (options, option)
        except Exception, e:
            pass

        try:
            for option in self.settings['options']:
                options = "%s --%s=%s" % (
                    options,
                    option,
                    self.settings['options'][option]
                )
        except Exception, e:
            pass

        return options

    def make_command_context_specific(self, command, directory):
        if os.getcwd() != directory:
            command = "pushd %s; %s; popd" % (directory, command)
        return command

    def run(self, context, args, contexts):
        if not args.subcommand:
            return self.default(context, args, contexts)
        return False


class CommandPasser(Command):
    """
    Like the Command object, but will pass commands to a given
    system command
    """
    base_dir = None

    def post_run(self, context, args, contexts, path, command):
        pass

    def pre_run(self, context, args, contexts, path):
        pass

    def run(self, context, args, contexts):
        options = self.get_options()
        if self.base_dir:
            # first try to set the path to something in the context (like web,
            # git, etc) and if that fails assume this is a filesystem path
            try:
                path = os.path.expanduser(context[self.base_dir])
            except KeyError, e:
                path = os.path.expanduser(self.base_dir)

            self.pre_run(context, args, context, path)

            # build the command
            command = "%s%s %s" % (
                self.command,
                options,
                " ".join(args.subcommand)
            )
            if self.environment:
                for env in self.environment:
                    command = "%s='%s' %s" % (env, self.environment[env], command)
            if self.ssh:
                command = """ssh %s "%s" """ % (self.ssh, command)

            print self.make_command_context_specific(
                command,
                path
            )

            self.post_run(context, args, context, path, command)
