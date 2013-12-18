import os
import sys

class Observable(object):
    def __init__(self):
        self.callbacks = {}

    def subscribe(self, event, callback):
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)

    def trigger(self, event, *args):
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                callback(args)

class Command(object):
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

class CommandPasser(object):
    """Like the Command object, but will pass commands to a given system command"""
    pass
