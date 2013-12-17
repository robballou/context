from context_commands import Command

class Contexts(Command):
    """List loaded contexts"""
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
