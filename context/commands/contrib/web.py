import os
from context.commands import Command

class Web(Command):
    alias = 'w'

    def default(self, context, args, contexts):
        print("cd %s" % os.path.expanduser(context['web']))
        return True

    def run(self, context, args, contexts):
        return_value = super(Web, self).run(context, args, contexts)
        if return_value:
            return

        if args.subcommand:
            web_directory = os.path.expanduser(context['web'])
            theme_directory = os.path.expanduser(context['theme'])
            if args.subcommand[0] == 'edit':
                print("$EDITOR %s" % web_directory)
            elif args.subcommand and args.subcommand[0] == 'finder':
                print("open %s" % web_directory)
            elif args.subcommand[0] == 'theme' and len(args.subcommand) == 1:
                print("cd %s" % theme_directory)
            elif args.subcommand[0] == 'theme' and len(args.subcommand) > 1:
                if args.subcommand[1] == 'finder':
                    print("open %s" % theme_directory)
                else:
                    print("cd %s" % theme_directory)

