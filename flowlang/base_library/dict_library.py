from ..core import ExecutableNode, VarParam, Variable
from ..library import register_type


@register_type
class ClearDict(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, dict())
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        d.clear()


@register_type
class CopyDict(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, dict())
            },
            output_params = 
            {
                'dict': VarParam('dict', dict, dict())
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        self.output_values['dict'].set_value(d.copy())


@register_type
class GetDictSize(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, dict())
            },
            output_params = 
            {
                'size': VarParam('size', int, int())
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        self.output_values['size'].set_value(len(d))


@register_type
class GetItemsFromDict(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, dict())
            },
            output_params = 
            {
                'items': VarParam('items', list, list())
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        self.output_values['items'].set_value(list(d.items()))


@register_type
class GetKeysFromDict(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, dict())
            },
            output_params = 
            {
                'keys': VarParam('keys', list, list())
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        self.output_values['keys'].set_value(list(d.keys()))


@register_type
class GetValuesFromDict(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, dict())
            },
            output_params = 
            {
                'values': VarParam('values', list, list())
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        self.output_values['values'].set_value(list(d.values()))


@register_type
class GetItemFromDict(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, ''),
                'key': VarParam('key', object, None)
            },
            output_params = 
            {
                'value': VarParam('value', object, None)
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        key = self.input_values['key'].get_value()
        self.output_values['value'].set_value(d.get(key))


@register_type
class AddItemToDict(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, ''),
                'key': VarParam('key', object, None),
                'value': VarParam('key', object, None)
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        key = self.input_values['key'].get_value()
        value = self.input_values['value'].get_value()
        d[key] = value


@register_type
class RemoveItemFromDict(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, ''),
                'key': VarParam('key', object, None)
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        key = self.input_values['key'].get_value()
        d.pop(key)

@register_type
class IsDictContainsKey(ExecutableNode):
    def __init__(self):
        super().__init__(
            input_params = 
            {
                'dict': VarParam('dict', dict, ''),
                'key': VarParam('key', object, None)
            },
            output_params=
            {
                'contains': VarParam('contains', bool, False)
            })

    def _execute(self, **kwargs):
        d = self.input_values['dict'].get_value()
        key = self.input_values['key'].get_value()
        self.output_values['contains'].set_value(key in d)
