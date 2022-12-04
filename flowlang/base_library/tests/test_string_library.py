import unittest

from ..string_library import *

class TestStringLibrary(unittest.TestCase):
    def test_split_node(self):
        node = StringSplitNode()
        node.set_input_value('str', Variable(str, '1.2.3'))
        node.set_input_value('sep', Variable(str, '.'))
        node()
        self.assertEqual(len(node.get_output_value('elements').get_value()), 3)