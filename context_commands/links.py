from context_commands import Command

class Links(Command):
    alias = 'l'
    def run(self, context, args, current_context):
        if not args.subcommand:
            print "echo Please enter a link name: context link name"
        elif args.subcommand[0] in context['links']:
            print "open %s" % context['links'][args.subcommand[0]]
        else:
            print "echo Link not found: %s" % args.subcommand[0]
