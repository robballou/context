import os
import sys
from context_commands import Command

class Bundler(Command):
    """Bundler commands"""
    alias = 'b'

    def run(self, context, args, current_context):
        theme_directory = os.path.expanduser(context['theme'])
        if not args.subcommand:
            self.error_message("No default command")
            sys.exit(1)
        else:
            print "pushd %s && bundle exec %s && popd" % (theme_directory, " ".join(args.subcommand))
