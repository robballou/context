import os
import sys

class Event(object):
    def __init__(self, context, **kwargs):
        self.context = context
        self.attributes = {}
        for kwarg in kwargs:
            self.attributes[kwarg] = kwargs[kwarg]

class Observable(object):
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

    def default(self, context, args, contexts):
        pass

    def error_message(self, message):
        sys.stderr.write("%s\n" % message)

    def make_command_context_specific(self, command, directory):
        if os.getcwd() != directory:
            command = "pushd %s; %s; popd" % (directory, command)
        return command

    def run(self, context, args, contexts):
        if not args.subcommand:
            return self.default(context, args, contexts)
        return False

class CommandPasser(Command):
    """Like the Command object, but will pass commands to a given system command"""
    base_dir = None

    def run(self, context, args, contexts):
        if self.base_dir:
            path = os.path.expanduser(context[self.base_dir])
            print self.make_command_context_specific("python manage.py %s" % " ".join(args.subcommand), path)
