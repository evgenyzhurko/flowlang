import logging
from .core import Node, Variable, ExecutableNode, VarParam
from .library import register_type


@register_type
class IncrementNode(ExecutableNode):
    def __init__(self, dtype=int):
        super().__init__(
            input_params = { 'value': VarParam('value', dtype, dtype()) },
            output_params = { 'value': VarParam('value', dtype, dtype()) })

    def _execute(self, **kwargs):
        value = self.input_values['value'].get_value()
        new_value = value + 1
        self.output_values['value'].set_value(new_value)
 

@register_type
class PrintNode(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params={ 'msg': VarParam('msg', object, '') }
        )

    def _execute(self, **kwargs):
        msg = self.input_values['msg'].get_value()
        print(f'Print node: message={msg}')


@register_type
class ForNode(ExecutableNode):
    def __init__(self):
        super().__init__(
            { 
                'start': VarParam('start', int, 0),
                'end': VarParam('end', int, 1),
                'step': VarParam('step', int, 1) 
            },
            {
                'finally': VarParam('finally', Node, None, callable=True),
                'index': VarParam('index', int, 0) 
            })

    def __call__(self, **kwargs):
        start = self.input_values['start'].get_value()
        end = self.input_values['end'].get_value()
        step = self.input_values['step'].get_value()
        iteration_exec = self.output_values['exec'].get_value()
        for i in range(start, end, step):
            self.output_values['index'].set_value(i)
            if iteration_exec is not None:
                iteration_exec(**kwargs)
        
        finally_exec = self.output_values['finally'].get_value()
        if finally_exec is not None:
            finally_exec(**kwargs)


@register_type
class IfElseNode(Node):
    def __init__(self):
        super().__init__(
            {
                'exec': VarParam('exec', Node, None, callable=True),
                'value': VarParam('value', bool, True),
            },
            {
                'true': VarParam('true', Node, None, callable=True),
                'false': VarParam('false', Node, None, callable=True)
            })

    def __call__(self, **kwargs):
        true_exec = self.output_values['true'].get_value()
        false_exec = self.output_values['false'].get_value()
        value = self.input_values['value'].get_value()
        if value:
            true_exec(**kwargs) if true_exec is not None else None
        else:
            false_exec(**kwargs) if false_exec is not None else None

@register_type
class SetVariableValue(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params={
                'value': VarParam('value', object, None),
                'variable': VarParam('variable', object, None)
            }
        )

    def _execute(self, **kwargs):
        self.get_input_value('variable').set_value(self.get_input_value('value').get_value())


@register_type
class GetInputArgument(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params={ 'name': VarParam('name', str, '') },
            output_params={ 'object': VarParam('object', object, None) }
        )

    def _execute(self, **kwargs):
        arg_name = self.get_input_value('name').get_value()
        self.get_output_value('object').set_value(kwargs[arg_name] if arg_name in kwargs else None)