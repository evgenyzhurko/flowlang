import unittest

from ..math_library import *

class TestMathLibraryWithIntVariables(unittest.TestCase):
    def setUp(self) -> None:
        self.var1 = Variable(int, 1)
        self.var2 = Variable(int, 2)

    def test_addition_node(self):
        node = AdditionNode()
        node.set_input_value('value1', self.var1)
        node.set_input_value('value2', self.var2)
        node()
        self.assertEqual(node.get_output_value('value').get_value(), 3)

    def test_substraction_node(self):
        node = SubstractionNode()
        node.set_input_value('value1', self.var1)
        node.set_input_value('value2', self.var2)
        node()
        self.assertEqual(node.get_output_value('value').get_value(), -1)

    def test_multiplication_node(self):
        node = MultiplicationNode()
        node.set_input_value('value1', self.var1)
        node.set_input_value('value2', self.var2)
        node()
        self.assertEqual(node.get_output_value('value').get_value(), 2)

    def test_division_node(self):
        node = DivisionNode()
        node.set_input_value('value1', self.var1)
        node.set_input_value('value2', self.var2)
        node()
        self.assertEqual(node.get_output_value('value').get_value(), 0.5)

    def test_floor_division(self):
        node = FloorDivisionNode()
        node.set_input_value('value1', self.var1)
        node.set_input_value('value2', self.var2)
        node()
        self.assertEqual(node.get_output_value('value').get_value(), 0)

    def test_modus(self):
        node = ModusNode()
        node.set_input_value('value1', self.var1)
        node.set_input_value('value2', self.var2)
        node()
        self.assertEqual(node.get_output_value('value').get_value(), 1)

    def test_exponent(self):
        node = ExponentNode()
        node.set_input_value('value1', self.var1)
        node.set_input_value('value2', self.var2)
        node()
        self.assertEqual(node.get_output_value('value').get_value(), 1)

    def test_equal1(self):
        node = EqualNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 2))
        node()
        self.assertFalse(node.get_output_value('value').get_value())

    def test_equal2(self):
        node = EqualNode()
        node.set_input_value('value1', Variable(int, 2))
        node.set_input_value('value2', Variable(int, 1))
        node()
        self.assertFalse(node.get_output_value('value').get_value())

    def test_equal3(self):
        node = EqualNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 1))
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_not_equal(self):
        node = NotEqualNode()
        node.set_input_value('value1', self.var1)
        node.set_input_value('value2', self.var2)
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_greater(self):
        node = GreaterNode()
        node.set_input_value('value1', self.var1)
        node.set_input_value('value2', self.var2)
        node()
        self.assertFalse(node.get_output_value('value').get_value())

    def test_greater_or_equal1(self):
        node = GreaterOrEqualNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 2))
        node()
        self.assertFalse(node.get_output_value('value').get_value())

    def test_greater_or_equal2(self):
        node = GreaterOrEqualNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 1))
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_less(self):
        node = LessNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 2))
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_less_or_equal(self):
        node = LessOrEqualNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 2))
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_binary_and(self):
        node = BinaryAndNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 3))
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_binary_and2(self):
        node = BinaryAndNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 2))
        node()
        self.assertFalse(node.get_output_value('value').get_value())

    def test_binary_or(self):
        node = BinaryOrNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 2))
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_binary_xor(self):
        node = BinaryXorNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 2))
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_binary_xor2(self):
        node = BinaryXorNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 1))
        node()
        self.assertFalse(node.get_output_value('value').get_value())

    def test_left_shift(self):
        node = LeftShiftNode()
        node.set_input_value('value1', Variable(int, 1))
        node.set_input_value('value2', Variable(int, 2))
        node()
        self.assertEqual(node.get_output_value('value').get_value(), 4)

    def test_right_shift(self):
        node = RightShiftNode()
        node.set_input_value('value1', Variable(int, 4))
        node.set_input_value('value2', Variable(int, 2))
        node()
        self.assertEqual(node.get_output_value('value').get_value(), 1)

    def test_logical_and(self):
        node = LogicalAndNode()
        node.set_input_value('value1', Variable(bool, True))
        node.set_input_value('value2', Variable(bool, True))
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_logical_and2(self):
        node = LogicalAndNode()
        node.set_input_value('value1', Variable(bool, True))
        node.set_input_value('value2', Variable(bool, False))
        node()
        self.assertFalse(node.get_output_value('value').get_value())

    def test_logical_or(self):
        node = LogicalOrNode()
        node.set_input_value('value1', Variable(bool, True))
        node.set_input_value('value2', Variable(bool, False))
        node()
        self.assertTrue(node.get_output_value('value').get_value())

    def test_logical_not(self):
        node = LogicalInversionNode()
        node.set_input_value('value', Variable(bool, True))
        node()
        self.assertFalse(node.get_output_value('value').get_value())

    def test_is(self):
        node = IsNode()
        node.set_input_value('value1', Variable(int, 0))
        node.set_input_value('value2', Variable(int, 1))
        node()
        self.assertFalse(node.get_output_value('value').get_value())
