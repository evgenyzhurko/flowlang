import unittest

from .. import Link, ExecutionLink, IncrementNode

class TestLinks(unittest.TestCase):
    def test_links_class_names_from_types(self):
        self.assertNotEqual(Link.get_class_name(), ExecutionLink.get_class_name())

    def test_class_names_from_objects(self):
        node1 = IncrementNode()
        node2 = IncrementNode()

        link = Link(node1, 'value', node2, 'value')
        exec_link = ExecutionLink(node1, node2)

        self.assertEqual(link.get_class_name(), Link.get_class_name())
        self.assertEqual(exec_link.get_class_name(), ExecutionLink.get_class_name())
        self.assertNotEqual(link.get_class_name(), exec_link.get_class_name())