class Command(object):
    def default(self, context, args):
        pass

    def run(self, context, args):
        if not args.subcommand:
            return self.default(context, args)
        return False
