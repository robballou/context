import os
from context.commands import CommandPasser

class Vagrant(CommandPasser):
    """Vagrant commands"""
    alias = 'v'
    base_dir = 'vagrant'
    command = 'vagrant'

    def run(self, context, args, contexts):
        vagrant_directory = os.path.expanduser(context['vagrant'])
        if not args.subcommand:
            print "cd %s" % vagrant_directory
        elif args.subcommand[0] == 'down':
            print self.make_command_context_specific('vagrant halt', vagrant_directory)
        else:
            super(Vagrant, self).run(context, args, contexts)
