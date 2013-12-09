import os
from context_commands import Command

class Vagrant(Command):
    """Vagrant commands"""
    alias = 'v'
    def run(self, context, args, current_context):
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
