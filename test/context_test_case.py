import unittest

class ContextTestCase(unittest.TestCase):
    def get_args(self, args_dict):
        class AttributeDict(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        return AttributeDict(args_dict)
