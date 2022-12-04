import unittest

from ..list_library import *


class TestListLibrary(unittest.TestCase):
    def setUp(self) -> None:
        self.var = Variable(list, [1,2,3,4,5,6,7,8,9])

    def test_slice(self):
        node = SliceNode()
        node.set_input_value('value', self.var)
        node.set_input_value('from', Variable(int, 1))
        node.set_input_value('to', Variable(int, 5))
        node()
        self.assertNotEqual(node.get_output_value('value').get_value(),
                            len(self.var.get_value()))

    def test_element_access(self):
        node = ValueAtNode()
        node.set_input_value('value', self.var)
        node.set_input_value('param', Variable(int, 5))
        node()
        self.assertEqual(node.get_output_value('value').get_value(), 6)

    def test_append_value(self):
        node = AppendValueNode()
        node.set_input_value('value', self.var)
        node.set_input_value('param', Variable(int, 100))
        node()
        self.assertTrue(100 in self.var.get_value())