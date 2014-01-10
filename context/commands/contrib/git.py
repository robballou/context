import os
from context.commands import Command

class Git(Command):
    """Git commands"""
    alias = 'g'

    def run(self, context, args, contexts):
        git_directory = os.path.expanduser(context['git'])
        if not args.subcommand:
            if os.getcwd() != git_directory:
                print "cd %s" % git_directory
        elif args.subcommand and args.subcommand[0] == 'edit':
            print "$EDITOR %s" % git_directory
        elif args.subcommand and args.subcommand[0] == 'finder':
            print "open %s" % git_directory
        else:
            # pass the command up to git, but run it in the correct context
            print self.make_command_context_specific("git %s" % " ".join(args.subcommand), git_directory)
