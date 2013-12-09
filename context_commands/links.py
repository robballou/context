from context_commands import Command

class Links(Command):
    alias = 'l'
    def run(self, context, args, contexts):
        if not args.subcommand:
            self.error_message("Links:")
            links = context['links'].keys()
            links.sort()
            for link in links:
                self.error_message("\t%s" % link)
        elif args.subcommand[0] in context['links']:
            print "open %s" % context['links'][args.subcommand[0]]
        else:
            print "echo Link not found: %s" % args.subcommand[0]
