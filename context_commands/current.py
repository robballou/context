from context_commands import Command

class Current(Command):
    """Current command"""
    def default(self, context, args, current_context):
        self.error_message(current_context)
        pass
