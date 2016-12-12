import os.path
from context.commands import CommandPasser

class Shell(CommandPasser):
    """Shell commands"""
    base_dir = 'git'
    command = 'shell'
    alias = 'sh'

    def run(self, context, args, contexts):
        options = self.get_options()
        if self.base_dir:
            # first try to set the path to something in the context (like web,
            # git, etc) and if that fails assume this is a filesystem path
            try:
                path = os.path.expanduser(context[self.base_dir])
            except KeyError as e:
                path = os.path.expanduser(self.base_dir)

            self.pre_run(context, args, context, path)

            # build the command
            command = "%s%s %s" % (
                '$SHELL',
                options,
                " ".join(args.subcommand)
            )
            if self.environment:
                for env in self.environment:
                    command = "%s='%s' %s" % (env, self.environment[env], command)
            if self.ssh:
                command = """ssh %s "%s" """ % (self.ssh, command)

            print(self.make_command_context_specific(
                command,
                path
            ))

            self.post_run(context, args, context, path, command)
