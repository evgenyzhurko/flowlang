import uuid

def register_type(cls):
    Library().add_node(cls)
    return cls

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Library(metaclass=Singleton):
    def __init__(self):
        self.uid = uuid.uuid4()
        self.nodes = {}

    def add_node(self, dtype):
        self.nodes[dtype.get_class_path()] = dtype

    def add_nodes(self, dtypes):
        for dtype in dtypes:
            self.add_node(dtype)

    def has_node(self, name):
        return name in self.nodes

    def get_type(self, name):
        return self.nodes[name]
