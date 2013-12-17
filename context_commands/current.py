from context_commands import Command

class Current(Command):
    """Display the current context"""
    def default(self, context, args, contexts):
        self.error_message(contexts.current_context)
