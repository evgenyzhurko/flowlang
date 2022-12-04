from ..core import ExecutableNode, VarParam, Variable
from ..library import register_type


@register_type
class StringSplitNode(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'str': VarParam('str', str, str()),
                'sep': VarParam('sep', str, str()) 
            },
            output_params =
            {
                'elements': VarParam('elements', list, list())
            })

    def _execute(self, **kwargs):
        s = self.input_values['str'].get_value()
        separator = self.input_values['sep'].get_value()
        result = s.split(separator)
        self.output_values['elements'].set_value(result)
