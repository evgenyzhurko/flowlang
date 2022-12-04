from ..core import ExecutableNode, VarParam, Variable
from ..library import register_type


class BaseListOperator(ExecutableNode):
    def __init__(self, f):
        super().__init__(
            input_params = 
            {
                'value': VarParam('value', list, list()),
                'param': VarParam('param', object, None) 
            },
            output_params = 
            {
                'value': VarParam('value', list, [])
            })
        self.f = f

    def _execute(self, **kwargs):
        value1 = self.input_values['value'].get_value()
        value2 = self.input_values['param'].get_value()
        result = self.f(value1, value2)
        self.output_values['value'].set_value(result)


class EmptyListOperator(ExecutableNode):
    def __init__(self, f):
        super().__init__(
            input_params = 
            {
                'value': VarParam('value', list, list())
            },
            output_params = 
            {
                'value': VarParam('value', list, list())
            })
        self.f = f

    def _execute(self, **kwargs):
        value = self.input_values['value'].get_value()
        result = self.f(value)
        self.output_values['value'].set_value(result)

@register_type
class SliceNode(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'value': VarParam('value', list, list()),
                'from': VarParam('from', int, 0),
                'to': VarParam('to', int, 0) 
            },
            output_params = 
            {
                'value': VarParam('value', list, list())
            })

    def _execute(self, **kwargs):
        value = self.input_values['value'].get_value()
        from_index = self.input_values['from'].get_value()
        to_index = self.input_values['to'].get_value()
        result = value[from_index:to_index]
        self.output_values['value'].set_value(result)


@register_type
class LeftSliceNode(BaseListOperator):
    def __init__(self):
        super().__init__(f = lambda x, y: x[:y])

@register_type
class RightSliceNode(BaseListOperator):
    def __init__(self):
        super().__init__(f = lambda x, y: x[y:])

@register_type
class ValueAtNode(BaseListOperator):
    def __init__(self):
        super().__init__(f = lambda x, y: x[y])

@register_type
class AppendValueNode(BaseListOperator):
    def __init__(self):
        super().__init__(f = lambda x, y: x.append(y))

@register_type
class ClearListNode(EmptyListOperator):
    def __init__(self):
        super().__init__(f = lambda x: x.clear())

@register_type
class Length(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'value': VarParam('value', list, [])
            },
            output_params = 
            {
                'length': VarParam('length', int, 0)
            })

    def _execute(self, **kwargs):
        value = self.input_values['value'].get_value()
        self.output_values['length'].set_value(len(value))