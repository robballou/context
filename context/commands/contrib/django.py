from context.commands import CommandPasser

class Django(CommandPasser):
    """Django commands"""
    alias = 'd'
    base_dir = 'web'
    command = 'python manage.py'
