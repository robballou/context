import subprocess
import re
import sys
from argparse import Namespace
from context.plugins import Plugin

class AutomaticSwitchToGit(Plugin):
    """
    Plugin to switch to the git folder automatically when switching.
    """
    def __init__(self, context_object):
        super(AutomaticSwitchToGit, self).__init__(context_object)
        # context_object.subscribe('switch.pre', self.switch)
        context_object.subscribe('switch', self.post_switch)
        self.context = context_object

    def post_switch(self, event):
        # check vbox manage
        event.context.run_command('git', Namespace(subcommand=[]))
