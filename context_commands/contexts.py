import sys
from context_commands import Command

class Contexts(Command):
    """List contexts"""
    def default(self, context, args, contexts):
        sys.stderr.write("Contexts:\n")
        context_keys = []
        for context_key in contexts.contexts:
            context_keys.append(context_key)

        context_keys.sort()
        for context_key in context_keys:
            sys.stderr.write("\t%s\n" % context_key)
