import sys

class Command(object):
    def default(self, context, args, current_context):
        pass

    def error_message(self, message):
        sys.stderr.write("%s\n" % message)

    def run(self, context, args, current_context):
        if not args.subcommand:
            return self.default(context, args, current_context)
        return False
