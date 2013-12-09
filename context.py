#!/usr/bin/env python
import argparse
import json
import os
import sys
import importlib

class Contexts(object):
    """
    Global contexts class
    """

    #
    # METHODS
    #
    def __init__(self, data=None):
        self.contexts = {}
        self.current_context = None
        self.registered_commands = {}
        self.command_aliases = {}

        if data:
            self.parse(data)

        # load commands
        commands = [
            "context_commands.bundler",
            "context_commands.current",
            "context_commands.git",
            "context_commands.links",
            "context_commands.vagrant",
            "context_commands.web",
            "context_commands.www",
        ]

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

        contexts_data_file = self.get_contexts_data_file()
        if os.path.exists(contexts_data_file):
            contexts_data = json.loads(open(contexts_data_file, 'r').read())
            if 'current_context' in contexts_data:
                self.current_context = contexts_data['current_context']

    def clear(self):
        os.unlink(self.get_contexts_data_file())

    def get(self, context=None):
        # contexts can't start with "_"
        if context.startswith('_'):
            return False

        if not context and self.current_context:
            return self.contexts[self.current_context]

        if context in self.contexts:
            return self.contexts[context]
        return False

    def get_contexts_data_file(self):
        return os.path.expanduser('~/.contexts-data')

    def help(self):
        """
        Display some usage and command information
        """
        sys.stderr.write("Usage: context [command] [subcommand ...]\n\n")
        sys.stderr.write("Commands:\n")
        commands = self.registered_commands.keys()
        commands.sort()
        for command in commands:
            this_command = command
            try:
                this_command = "%s (%s)" % (this_command, self.registered_commands[command].alias)
            except AttributeError:
                pass
            sys.stderr.write("\t%s\n" % this_command)

    def parse(self, data):
        self.contexts = json.loads(data)

    def run_command(self, command, args):
        if command in self.registered_commands:
            this_command = self.registered_commands[command]
        elif command in self.command_aliases:
            this_command = self.registered_commands[self.command_aliases[command]]
        else:
            sys.stderr.write("Invalid command: %s\n" % command)
            sys.exit(1)
        command_object = this_command()
        command_object.run(self.get(self.current_context), args, self.current_context)

    def switch(self, context):
        if not self.get(context):
            raise Exception('Invalid context: %s' % context)

        self.current_context = context
        fp = open(self.get_contexts_data_file(), 'w')
        data = json.dumps({'current_context': self.current_context})
        fp.write(data)
        fp.close()

def context(args):
    """
    Context functionality from __main__

    This will get the global contexts object and run some basic system commands
    """
    contexts = load_contexts()

    if not args.command:
        contexts.help()
        sys.exit(0)

    if args.command == 'switch' and args.subcommand and not contexts.get(args.subcommand[0]):
        print "Could not find context: %s" % (args.subcommand[0])
        sys.exit(1)

    if args.command == 'switch':
        contexts.switch(args.subcommand[0])
    elif args.command == 'clear':
        contexts.clear()
    else:
        contexts.run_command(args.command, args)

def load_contexts():
    data_file = os.path.expanduser('~/.contexts')
    if not os.path.exists(data_file):
        return Contexts()

    data = open(data_file, 'r').read()
    return Contexts(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Context switcher')
    # add arguments
    parser.add_argument('command', help='Choose your command', nargs="?")
    parser.add_argument('subcommand', help='Choose your sub commands', nargs="*")
    args = parser.parse_args()
    context(args)
