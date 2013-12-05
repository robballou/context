import os
from context_commands import Command

class Git(Command):
    """Git commands"""
    alias = 'g'

    def run(self, context, args):
        git_directory = os.path.expanduser(context['git'])
        if not args.subcommand:
            print "cd %s" % git_directory
        else:
            print "pushd %s && git %s && popd" % (git_directory, " ".join(args.subcommand))
