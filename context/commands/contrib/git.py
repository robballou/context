import os
from context.commands import Command

class Git(Command):
    """Git commands"""
    alias = 'g'

    def parse_variables(self, command, branch_settings):
        """
        Replace variables in the command
        """
        command = self.contexts.parse_variables(command, self.context)
        command = command.replace('$branch', '$(git rev-parse --abbrev-ref HEAD)')
        command = command.replace('$date', '$(date +"%Y%m%d%H%M%S")')
        if 'db' in branch_settings:
            command = command.replace('$db', branch_settings['db'])
        return command

    def run(self, context, args, contexts):
        git_directory = os.path.expanduser(context['git'])
        if not args.subcommand:
            if os.getcwd() != git_directory:
                print("cd %s" % git_directory)
        elif args.subcommand and args.subcommand[0] == 'edit':
            print("$EDITOR %s" % git_directory)
        elif args.subcommand and args.subcommand[0] == 'finder':
            print("open %s" % git_directory)
        elif args.subcommand and (args.subcommand[0] == 'branch' or args.subcommand[0] == 'b'):
            # check if the branch is in our configuration
            if 'settings' in self.context and 'git' in self.context['settings'] and 'branch' in self.context['settings']['git']:
                branch_precommands = []
                branch_postcommands = []
                git_branch_settings = self.context['settings']['git']['branch']
                if '__defaults' in git_branch_settings:
                    if 'precommands' in git_branch_settings['__defaults']:
                        branch_precommands = git_branch_settings['__defaults']['precommands']
                    if 'postcommands' in git_branch_settings['__defaults']:
                        branch_postcommands = git_branch_settings['__defaults']['postcommands']

                this_branch_settings = None
                if args.subcommand[1] in git_branch_settings:
                    this_branch_settings = git_branch_settings[args.subcommand[1]]
                    if 'precommands' in this_branch_settings:
                        branch_precommands += this_branch_settings['precommands']
                    if 'postcommands' in this_branch_settings:
                        branch_postcommands += this_branch_settings['postcommands']

                # self.contexts.message(branch_precommands)
                # self.contexts.message(branch_postcommands)

                command = []
                for precommand in branch_precommands:
                    precommand = self.parse_variables(precommand, this_branch_settings)
                    command.append(precommand)

                command.append("git checkout %s" % (args.subcommand[1]))

                for postcommand in branch_postcommands:
                    postcommand = self.parse_variables(postcommand, this_branch_settings)
                    command.append(postcommand)

                command_string = " && ".join(command)
                print(self.make_command_context_specific(command_string, git_directory))
        else:
            # pass the command up to git, but run it in the correct context
            print(self.make_command_context_specific("git %s" % " ".join(args.subcommand), git_directory))
