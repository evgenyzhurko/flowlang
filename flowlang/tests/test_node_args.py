import unittest

from .. import GetInputArgument, Flow


class TestArguments(unittest.TestCase):
    def test_args_in_node(self):
        test_arg_value = [1, 2, 3]

        node = GetInputArgument()
        node.get_input_value('name').set_value('arg')
        node(arg=test_arg_value)

        val = node.get_output_value('object').get_value()
        self.assertEqual(val, test_arg_value)
        
    def test_invalid_args_in_node(self):
        node = GetInputArgument()
        node.get_input_value('name').set_value('arg')
        node(a=1)

        val = node.get_output_value('object').get_value()
        self.assertIsNone(val)

    def test_args_passing_to_flow(self):
        flow = Flow()

        node = GetInputArgument()
        node.get_input_value('name').set_value('arg')

        flow.add_node(node)
        flow.set_start(node)

        flow(arg='hello')

        val = node.get_output_value('object').get_value()
        self.assertEqual(val, 'hello')