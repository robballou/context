from context_commands import Command

class Web(Command):
    alias = 'w'
    def default(self, context, args):
        print "cd %s" % context['web']
