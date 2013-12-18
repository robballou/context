import subprocess
from context_plugins import Plugin

class Notify(Plugin):
    """Send notifications"""

    def __init__(self, context_object):
        context_object.subscribe('switch', self.switch)

    def notify(self, title, message):
        t = '-title {!r}'.format(title)
        m = '-message {!r}'.format(message)
        subprocess.call('terminal-notifier {}'.format(' '.join([m, t])), shell=True)

    def switch(self, context):
        self.notify('Context Switcher', 'Switched to context: %s' % context)
