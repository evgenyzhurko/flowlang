from ..library import register_type
from ..core import Node, VarParam, Variable


class BaseObjectNode(Node):
    def __init__(self, dtype):
        super().__init__(
            output_params = 
            {
                'value': VarParam('value', dtype, dtype(), editable=True)
            })

@register_type
class MakeIntNode(BaseObjectNode):
    def __init__(self):
        super().__init__(int)

@register_type
class MakeFloatNode(BaseObjectNode):
    def __init__(self):
        super().__init__(float)

@register_type
class MakeBoolNode(BaseObjectNode):
    def __init__(self):
        super().__init__(bool)

@register_type
class MakeStrNode(BaseObjectNode):
    def __init__(self):
        super().__init__(str)

@register_type
class MakeListNode(BaseObjectNode):
    def __init__(self):
        super().__init__(list)

@register_type
class MakeDictNode(BaseObjectNode):
    def __init__(self):
        super().__init__(dict)