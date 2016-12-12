import os.path
from context.commands import CommandPasser


class Drush(CommandPasser):
    """Drush commands"""
    base_dir = 'web'
    command = 'drush'
    alias = 'dr'

    def get_options(self):
        """Override CommandPasser.get_options to allow for Drush aliases"""
        options = super(Drush, self).get_options()

        # try to see if there is an alternate directory location
        try:
            self.base_dir = self.settings['directory']
        except Exception as e:
            pass

        # try to add the alias
        try:
            alias = self.settings['aliases']['default']
            if self.command_args and self.command_args in self.settings['aliases']:
                alias = self.settings['aliases'][self.command_args]
            if not isinstance(alias, dict):
                options = " @%s%s" % (alias, options)
            else:
                self.command = self.settings['aliases'][self.command_args]['command']
                if 'environment' in self.settings['aliases'][self.command_args].keys():
                    self.environment = self.settings['aliases'][self.command_args]['environment']
                if 'ssh' in self.settings['aliases'][self.command_args].keys():
                    self.ssh = self.settings['aliases'][self.command_args]['ssh']
        except Exception as e:
            pass
        return options

    # def pre_run(self, context, args, contexts, path):
    #     if self.settings['docker']:
    #         self.command = self.settings['docker']
