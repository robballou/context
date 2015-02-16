from context.commands import CommandPasser


class Drush(CommandPasser):
    """Drush commands"""
    base_dir = 'web'
    command = 'drush'
    alias = 'dr'

    def get_options(self):
        """Override CommandPasser.get_options to allow for Drush aliases"""
        options = super(Drush, self).get_options()

        # try to add the alias
        try:
            alias = self.settings['aliases']['default']
            if self.command_args and self.command_args in self.settings['aliases']:
                alias = self.settings['aliases'][self.command_args]
            options = " @%s%s" % (alias, options)
        except Exception, e:
            pass
        return options
