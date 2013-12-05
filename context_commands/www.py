from context_commands import Command

class Www(Command):
    def default(self, context, args):
        print "open %s" % context['www']
