import sys

class Command(object):
    def default(self, context, args, contexts):
        pass

    def error_message(self, message):
        sys.stderr.write("%s\n" % message)

    def run(self, context, args, contexts):
        if not args.subcommand:
            return self.default(context, args, contexts)
        return False

class CommandPasser(object):
    """Like the Command object, but will pass commands to a given system command"""
    pass
