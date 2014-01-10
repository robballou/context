import os
from context.commands import Command

class Edit(Command):
    """Edit commands"""
    alias = 'e'
    def default(self, context, args, contexts):
        print "$EDITOR %s" % os.path.expanduser(contexts.context_file)
