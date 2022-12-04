from ..library import register_type
from ..core import ExecutableNode, VarParam, Variable


class OneOperatorNode(ExecutableNode):
    def __init__(self, f, dtype=object):
        super().__init__(
            input_params = 
            {
                'value': VarParam('value', dtype, None)
            },
            output_params = 
            {
                'value': VarParam('value', dtype, None)
            })
        self.f = f

    def _execute(self, **kwargs):
        value = self.input_values['value'].get_value()
        result = self.f(value)
        self.output_values['value'].set_value(result)


class BaseOperatorNode(ExecutableNode):
    def __init__(self, f, dtype=object):
        super().__init__(
            input_params = 
            {
                'value1': VarParam('value1', dtype, None),
                'value2': VarParam('value2', dtype, None) 
            },
            output_params = 
            {
                'value': VarParam('value', dtype, None)
            })
        self.f = f

    def _execute(self, **kwargs):
        value1 = self.input_values['value1'].get_value()
        value2 = self.input_values['value2'].get_value()
        result = self.f(value1, value2)
        self.output_values['value'].set_value(result)
 

@register_type
class AdditionNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x + y)

@register_type
class SubstractionNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x - y)

@register_type
class MultiplicationNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x * y)

@register_type
class DivisionNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x / y)

@register_type
class FloorDivisionNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x // y)

@register_type
class ModusNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x % y)

@register_type
class ExponentNode(BaseOperatorNode):
    def __init__(self, dtype=int):
        super().__init__(lambda x, y: x ** y, dtype)

@register_type
class EqualNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x == y)

@register_type
class NotEqualNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x != y)

@register_type
class GreaterNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x > y)

@register_type
class GreaterOrEqualNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x >= y)

@register_type
class LessNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x < y)

@register_type
class LessOrEqualNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x <= y)

@register_type
class BinaryAndNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x & y)

@register_type
class BinaryOrNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x | y)

@register_type
class BinaryXorNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x ^ y)

@register_type
class LeftShiftNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x << y)

@register_type
class RightShiftNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x >> y)

@register_type
class LogicalAndNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x and y)

@register_type
class LogicalOrNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x or y)

@register_type
class LogicalInversionNode(OneOperatorNode):
    def __init__(self):
        super().__init__(lambda x: not x)

@register_type
class IsNode(BaseOperatorNode):
    def __init__(self):
        super().__init__(lambda x, y: x is y)
