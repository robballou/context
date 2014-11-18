import pprint
import sys

from context.commands import Command

class Contexts(Command):
    """List loaded contexts and view information about a context"""
    def default(self, context, args, contexts):
        self.error_message("Contexts:")
        context_keys = []
        for context_key in contexts.contexts:
            # skip contexts that start with "__" as those are
            # "system" entries
            if context_key.startswith('__'):
                continue
            context_keys.append(context_key)

        context_keys.sort()
        for context_key in context_keys:
            self.error_message("\t%s" % context_key)

    def run(self, context, args, contexts):
        # details about a specific context
        if args.subcommand:
            this_context = args.subcommand[0]
            pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)
            pp.pprint(contexts.contexts[this_context])
            return

        self.default(context, args, contexts)
