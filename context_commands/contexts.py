import sys
from context_commands import Command

class Contexts(Command):
    """List contexts"""
    def default(self, context, args, contexts):
        self.error_message("Contexts:")
        context_keys = []
        for context_key in contexts.contexts:
            context_keys.append(context_key)

        context_keys.sort()
        for context_key in context_keys:
            self.error_message("\t%s" % context_key)
