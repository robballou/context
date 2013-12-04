#!/usr/bin/env python
import argparse
import json
import os
import sys

class Command(object):
    def default(self, context, args):
        pass

    def run(self, context, args):
        if not args.subcommand:
            return self.default(context, args)
        return False

class Contexts(object):
    """
    Global contexts class
    """

    class Git(Command):
        """Git commands"""
        def run(self, context, args):
            print "cd %s" % os.path.expanduser(context['git'])

    class Vagrant(Command):
        """Vagrant commands"""
        def run(self, context, args):
            vagrant_directory = os.path.expanduser(context['vagrant'])
            # by default, go to the vagrant directory
            if not args.subcommand:
                print "cd %s" % vagrant_directory
            elif args.subcommand[0] == 'down' or args.subcommand[0] == 'halt':
                print "pushd %s && vagrant halt && popd" % vagrant_directory
            elif args.subcommand[0] == 'up':
                print "pushd %s && vagrant up && popd" % vagrant_directory
            elif args.subcommand[0] == 'ssh':
                print "pushd %s && vagrant ssh && popd" % vagrant_directory
            elif args.subcommand[0] == 'status':
                print "pushd %s && vagrant status && popd" % vagrant_directory

    def __init__(self, data=None):
        self.contexts = {}
        self.current_context = None

        if data:
            self.parse(data)

        contexts_data_file = self.get_contexts_data_file()
        if os.path.exists(contexts_data_file):
            contexts_data = json.loads(open(contexts_data_file, 'r').read())
            if 'current_context' in contexts_data:
                self.current_context = contexts_data['current_context']

    def clear(self):
        os.unlink(self.get_contexts_data_file())

    def get(self, context=None):
        if not context and self.current_context:
            return self.contexts[self.current_context]

        if context in self.contexts:
            return self.contexts[context]
        return False

    def get_contexts_data_file(self):
        return os.path.expanduser('~/.contexts-data')

    def parse(self, data):
        self.contexts = json.loads(data)

    def run_command(self, command, args):
        command_class = command.title().replace(" ", "")
        command_object = getattr(self, command_class)()
        command_object.run(self.get(self.current_context), args)

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
    if args.command == 'switch' and args.subcommand and not contexts.get(args.subcommand[0]):
        print "Could not find context: %s" % (args.subcommand[0])
        sys.exit(1)

    if args.command == 'switch':
        contexts.switch(args.subcommand[0])
    elif args.command == 'current':
        print "echo %s" % contexts.current_context
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
    parser.add_argument('command', help='Choose your command')
    parser.add_argument('subcommand', help='Choose your sub commands', nargs="*")
    args = parser.parse_args()
    context(args)
