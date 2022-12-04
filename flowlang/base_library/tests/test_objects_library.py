import unittest

from ..objects_library import *


class TestStringLibrary(unittest.TestCase):
    def test_split_node(self):
        node = MakeIntNode()
        node.get_output_param('value').default_value = 5
        node.get_output_value('value').set_value(5)

        node2 = MakeIntNode()
        node2.from_dict(node.to_dict())

        self.assertEqual(node.to_dict(), node2.to_dict())
