import os
from context.commands import Command

class Vagrant(Command):
    """Vagrant commands"""
    alias = 'v'
    def run(self, context, args, contexts):
        vagrant_directory = os.path.expanduser(context['vagrant'])
        # by default, go to the vagrant directory
        if not args.subcommand:
            print "cd %s" % vagrant_directory
        elif args.subcommand[0] == 'down' or args.subcommand[0] == 'halt':
            print self.make_command_context_specific("vagrant halt", vagrant_directory)
        elif args.subcommand[0] == 'up':
            print self.make_command_context_specific("vagrant up", vagrant_directory)
        elif args.subcommand[0] == 'ssh':
            print self.make_command_context_specific("vagrant ssh", vagrant_directory)
        elif args.subcommand[0] == 'status':
            print self.make_command_context_specific("vagrant status", vagrant_directory)
