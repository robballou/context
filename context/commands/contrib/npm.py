from context.commands import CommandPasser

class Npm(CommandPasser):
    """NPM commands"""
    base_dir = 'git'
    command = 'npm'
