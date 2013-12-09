from context_commands import Command

class Www(Command):
    def default(self, context, args, current_context):
        print "open %s" % context['www']
