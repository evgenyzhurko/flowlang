import unittest

from .. import IncrementNode, ReturnNode, Flow, Link, ExecutionLink


class TestReturnValue(unittest.TestCase):
    def test_args_in_node(self):
        node1 = IncrementNode()
        node2 = ReturnNode()

        link1 = Link(node1, 'value', node2, 'object')
        link2 = ExecutionLink(node1, node2)

        flow = Flow()
        flow.add_nodes([node1, node2])
        flow.add_links([link1, link2])
        flow.set_start(node1)
        result = flow()

        self.assertEqual(result, 1)
        