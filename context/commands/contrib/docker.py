from context.commands import CommandPasser

class Docker(CommandPasser):
    """Docker commands"""
    base_dir = 'git'
    command = 'docker'

    def run(self, context, args, contexts):
        if context['docker'] == 'drocker':
            if not self.contexts.file_exists('drocker', context):
                self.command = 'drocker'
            else:
                self.command = './drocker'
        elif context['docker'] == 'compose':
            self.command = 'docker-compose'

        super(Docker, self).run(context, args, contexts)
