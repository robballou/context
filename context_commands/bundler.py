import os
import sys
from context_commands import Command

class Bundler(Command):
    """Bundler commands"""
    alias = 'b'

    def run(self, context, args):
        theme_directory = os.path.expanduser(context['theme'])
        if not args.subcommand:
            sys.stderr.write("No default command\n")
            sys.exit(1)
        else:
            print "pushd %s && bundle exec %s && popd" % (theme_directory, " ".join(args.subcommand))
