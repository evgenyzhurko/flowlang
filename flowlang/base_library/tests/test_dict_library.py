import unittest

from ..dict_library import *

class TestDictLibrary(unittest.TestCase):
    def setUp(self) -> None:
        self.var = Variable(dict, dict())
        self.var.set_value({
            1:1,
            2:2,
            3:3
        })

    def test_get_size_node(self):
        node = GetDictSize()
        node.set_input_value('dict', self.var)
        node()
        out_var = node.get_output_value('size')
        self.assertEqual(out_var.get_value(), len(self.var.get_value()))

    def test_clear_dict_node(self):
        node = ClearDict()
        node.set_input_value('dict', self.var)
        node()
        self.assertEqual(0, len(self.var.get_value()))

    def test_copy_dict_node(self):
        node = CopyDict()
        node.set_input_value('dict', self.var)
        node()
        out_var = node.get_output_value('dict')
        self.assertEqual(out_var.get_value(), self.var.get_value())
        self.var.get_value()[4] = 4
        self.assertNotEqual(out_var.get_value(), self.var.get_value())
    
    def test_get_items_dict(self):
        node = GetItemsFromDict()
        node.set_input_value('dict', self.var)
        node()
        out_var = node.get_output_value('items')
        self.assertEqual(type(out_var.get_value()), list)
        self.assertEqual(len(out_var.get_value()), len(self.var.get_value()))

    def test_get_keys_dict(self):
        node = GetKeysFromDict()
        node.set_input_value('dict', self.var)
        node()
        out_var = node.get_output_value('keys')
        self.assertEqual(type(out_var.get_value()), list)
        self.assertEqual(len(out_var.get_value()), len(self.var.get_value()))

    def test_get_values_dict(self):
        node = GetValuesFromDict()
        node.set_input_value('dict', self.var)
        node()
        out_var = node.get_output_value('values')
        self.assertEqual(type(out_var.get_value()), list)
        self.assertEqual(len(out_var.get_value()), len(self.var.get_value()))

    def test_get_item_by_key(self):
        node = GetItemFromDict()
        node.set_input_value('dict', self.var)
        node.get_input_value('key').set_value(1)
        node()
        out_var = node.get_output_value('value')
        self.assertEqual(out_var.get_value(), 1)
        
    def test_add_and_get_item_by_key(self):
        node = AddItemToDict()
        node.set_input_value('dict', self.var)
        node.get_input_value('key').set_value(5)
        node.get_input_value('value').set_value(5)
        node()
        self.assertTrue(5 in self.var.get_value())

    def test_add_and_get_item_by_key(self):
        node = RemoveItemFromDict()
        node.set_input_value('dict', self.var)
        node.get_input_value('key').set_value(3)
        node()
        self.assertFalse(3 in self.var.get_value())
