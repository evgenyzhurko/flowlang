import unittest

from .. import Library
from .. import ForNode


class TestLibrary(unittest.TestCase):
    def setUp(self) -> None:
        self.library = Library()

    def test_new_instance_of_library(self):
        lib = Library()
        self.assertEqual(lib.uid, self.library.uid)

    def test_instance_with_specific_import(self):
        from ..library import Library
        lib = Library()
        self.assertEqual(lib.uid, self.library.uid)

    def test_library_is_not_empty(self):
        self.assertTrue(self.library.has_node(ForNode.get_class_path()))
