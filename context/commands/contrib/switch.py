import sys
from context.commands import Command

class Switch(Command):
    """Switch the current context"""
    alias = 's'

    def run(self, context, args, contexts):
        contexts.switch(args.subcommand[0], args)
