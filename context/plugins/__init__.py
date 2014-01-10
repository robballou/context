import sys
from context_commands import Observable

class Plugin(Observable):
    def __init__(self, context_object):
        self.context_object = context_object

    def message(self, message):
        sys.stderr.write("%s\n" % message)
