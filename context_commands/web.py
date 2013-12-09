import os
from context_commands import Command

class Web(Command):
    alias = 'w'

    def default(self, context, args, contexts):
        print "cd %s" % os.path.expanduser(context['web'])
        return True

    def run(self, context, args, contexts):
        return_value = super(Web, self).run(context, args, contexts)
        if return_value:
            return

        if args.subcommand and args.subcommand[0] == 'edit':
            print "$EDITOR %s" % os.path.expanduser(context['web'])

