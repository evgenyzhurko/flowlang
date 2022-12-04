import unittest

from .. import Link, ExecutionLink, IncrementNode, Flow

class TestLinks(unittest.TestCase):
    def test_class_names_from_objects(self):
        node1 = IncrementNode()
        node2 = IncrementNode()
        node3 = IncrementNode()

        link1 = Link(node1, 'value', node2, 'value')
        link2 = Link(node2, 'value', node3, 'value')
        exec_link1 = ExecutionLink(node1, node2)
        exec_link2 = ExecutionLink(node2, node3)

        flow = Flow()
        flow.set_start(node1)
        flow.add_nodes([node1, node2, node3])
        flow.add_links([link1, link2, exec_link1, exec_link2])

        flow_serialized = Flow()
        flow_serialized.from_json(flow.to_json())

        flow()
        flow_serialized()
        
        self.assertEqual(
            flow.nodes[-1].get_output_value('value').get_value(),
            flow_serialized.nodes[-1].get_output_value('value').get_value(),
        )

