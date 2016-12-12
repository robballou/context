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
            print("cd %s" % vagrant_directory)
        elif args.subcommand[0] == 'down':
            print(self.make_command_context_specific('vagrant halt', vagrant_directory))
        elif args.subcommand[0] == 'ssh' and len(args.subcommand) > 1:
            # inject --command before the subsequent commands
            args.subcommand.insert(1, '--command')
            # make sure to quote the command
            args.subcommand[2] = '"%s' % args.subcommand[2]
            args.subcommand[-1] = '%s"' % args.subcommand[-1]
            super(Vagrant, self).run(context, args, contexts)
        else:
            super(Vagrant, self).run(context, args, contexts)
