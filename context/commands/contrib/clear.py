import os
from context.commands import Command

class Clear(Command):
    """Clear the current context"""
    def default(self, context, args, contexts):
        os.unlink(contexts.get_contexts_data_file())