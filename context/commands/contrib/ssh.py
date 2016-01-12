from context.commands import CommandPasser

class Ssh(CommandPasser):
    """SSH commands"""
    base_dir = 'git'
    command = 'ssh'

    def get_options(self):
        """Override CommandPasser.get_options to allow for SSH aliases"""
        options = super(Ssh, self).get_options()

        # try to add the host
        try:
            host = self.settings['default']
            if self.command_args and self.command_args in self.settings:
                host = self.settings[self.command_args]
            options = " %s%s" % (host, options)
        except Exception, e:
            pass
        return options
