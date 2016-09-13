import os.path
from context.commands import CommandPasser

class Bash(CommandPasser):
    """Bash commands"""
    base_dir = 'git'
    command = 'bash'
    alias = 'bs'
