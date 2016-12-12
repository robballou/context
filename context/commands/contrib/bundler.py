import os
import sys
from context.commands import Command

class Bundler(Command):
    """
    Bundler commands

    Passes commands up to bundler.
    """
    alias = 'b'

    def run(self, context, args, contexts):
        theme_directory = os.path.expanduser(context['theme'])
        if not args.subcommand:
            self.error_message("No default command")
            sys.exit(1)
        else:
            print(self.make_command_context_specific(" ".join(args.subcommand), theme_directory))
