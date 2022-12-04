import uuid
import json
import logging

import sys
import subprocess

from .library import Library


def resolve_dependencies(dependencies):
    for module in dependencies:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        finally:
            __import__(module)


class Variable:
    def __init__(self, dtype, default_value):
        assert(dtype is not None)
        self.dtype = dtype
        self.value = default_value
        self.default_value = default_value

    def get_type(self):
        return self.dtype

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def reset(self):
        self.value = self.default_value


class VarParam:
    def __init__(self, name, dtype, default_value, callable=False, editable=False):
        self.name = name
        self.dtype = dtype
        self.default_value = default_value
        self.callable = callable
        self.editable = editable


class Node:
    def __init__(self, input_params = {}, output_params={}):
        self.uuid = uuid.uuid4()

        self.x = 0
        self.y = 0
        
        self.input_params = input_params
        self.output_params = output_params

        self.input_values = {}
        self.output_values = {}

        for key, value in self.input_params.items():
            self.input_values[key] = Variable(value.dtype, value.default_value)

        for key, value in self.output_params.items():
            self.output_values[key] = Variable(value.dtype, value.default_value)

    @classmethod
    def get_class_type(cls):
        return cls

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    @classmethod
    def get_class_main_module(cls):
        return cls.__module__.split('.')[0]

    @classmethod
    def get_class_path(cls):
        return cls.__module__ + '.' + cls.__name__

    def _execute(self, **kwargs):
        pass

    def get_input_param(self, name):
        return self.input_params[name]

    def get_input_value(self, name):
        return self.input_values[name]

    def get_output_param(self, name):
        return self.output_params[name]

    def get_output_value(self, name):
        return self.output_values[name]

    def set_input_value(self, name, varible):
        self.input_values[name] = varible

    def reset_input_value(self, name):
        self.input_values[name] = Variable(
            self.input_params[name].dtype,
            self.input_params[name].default_value)

    def __call__(self, **kwargs):
        self._execute(**kwargs)
        logging.debug(f'{self.get_class_name()} executed')

    def to_dict(self):
        data = {}
        data['classpath'] = self.get_class_path()
        data['uuid'] = str(self.uuid)
        data['x'] = self.x
        data['y'] = self.y

        params = {}
        for key, value in self.input_params.items():
            if value.editable and value.default_value is not None:
                params[key] = value.default_value
        data['input_params'] = params

        params = {}
        for key, value in self.output_params.items():
            if value.editable and value.default_value is not None:
                params[key] = value.default_value
        data['output_params'] = params

        return data

    def from_dict(self, data):
        assert(data['classpath'] == self.get_class_path())
        self.uuid = uuid.UUID(data['uuid'])
        self.x = data['x']
        self.y = data['y']

        for key, _ in self.input_params.items():
            if key in data['input_params']:
                node_value = data['input_params'][key]
                self.input_params[key].default_value = self.input_params[key].dtype(node_value)
                self.input_values[key].set_value(self.input_params[key].default_value)

        for key, _ in self.output_params.items():
            if key in data['output_params']:
                node_value = data['output_params'][key]
                self.output_params[key].default_value = self.output_params[key].dtype(node_value)
                self.output_values[key].set_value(self.output_params[key].default_value)


class ExecutableNode(Node):
    def __init__(self, input_params = {}, output_params={}):
        input_params_with_exec = input_params
        input_params_with_exec['exec'] = VarParam('exec', Node, None, callable=True)
        output_params_with_exec = output_params
        output_params_with_exec['exec'] = VarParam('exec', Node, None, callable=True)

        super().__init__(input_params_with_exec, output_params_with_exec)

    def __call__(self, **kwargs):
        super().__call__(**kwargs)
        
        next_node = self.output_values['exec'].get_value()
        if next_node is not None:
            next_node(**kwargs)


class Link():
    def __init__(self, source: Node, source_name: str, destination: Node, destination_name: str):
        self.source = source
        self.destination = destination
        self.source_name = source_name
        self.destination_name = destination_name

        self.destination.set_input_value(
            self.destination_name,
            self.source.get_output_value(self.source_name))

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    def __del__(self):
        if self.destination is not None:
            self.destination.reset_input_value(self.destination_name)

    def to_dict(self):
        data = {}
        data['classname'] = self.get_class_name()
        data['source'] = str(self.source.uuid)
        data['source_name'] = self.source_name
        data['destination'] = str(self.destination.uuid)
        data['destination_name'] = self.destination_name
        return data


class ExecutionLink(Link):
    def __init__(self, source: ExecutableNode, destination: ExecutableNode, source_exec='exec', destination_exec='exec'):
        super().__init__(source, source_exec, destination, destination_exec)
        self.source_exec = source_exec
        self.destination_exec = destination_exec
        self.source.get_output_value(source_exec).set_value(self.destination)

    def __del__(self):
        super().__del__()
        self.source.get_output_value(self.source_exec).reset()


class Flow(Node):
    def __init__(self):
        super().__init__()

        self.nodes = []
        self.links = []

        self.start_node = None

    def get_flow_dependencies(self):
        deps = set()
        for node in self.nodes:
            deps.add(node.get_class_main_module())
        return list(deps)

    def to_dict(self):
        data = {}
        data['dependencies'] = self.get_flow_dependencies()
        data['nodes'] = [node.to_dict() for node in self.nodes]
        data['links'] = [link.to_dict() for link in self.links]

        if self.start_node is not Node:
            data['start'] = str(self.start_node.uuid)

        return json.dumps(data)

    def from_dict(self, data):
        data = json.loads(data)
        resolve_dependencies(data['dependencies'])

        for node in data['nodes']:
            node_object = Library().get_type(node['classpath'])()
            node_object.from_dict(node)
            self.nodes.append(node_object)

        for link in data['links']:
            if link['classname'] == Link.get_class_name():
                self.links.append(
                    Link(
                        self.get_node(uuid.UUID(link['source'])),
                        link['source_name'],
                        self.get_node(uuid.UUID(link['destination'])),
                        link['destination_name']
                    )
                )
            elif link['classname'] == ExecutionLink.get_class_name():
                self.links.append(
                    ExecutionLink(
                        self.get_node(uuid.UUID(link['source'])),
                        self.get_node(uuid.UUID(link['destination'])),
                        source_exec=link['source_name'],
                        destination_exec=link['destination_name']
                    )
                )

        if 'start' in data:
            self.start_node = self.get_node(uuid.UUID(data['start']))

    def to_json(self):
        return json.dumps(self.to_dict())

    def from_json(self, text):
        self.from_dict(json.loads(text))

    def add_node(self, node: Node):
        self.nodes.append(node)

    def get_node(self, uuid):
        return list(filter(lambda node: node.uuid == uuid, self.nodes))[0]

    def add_nodes(self, nodes: list):
        self.nodes.extend(nodes)

    def remove_node(self, node: Node):
        self.nodes.remove(node)

    def add_link(self, link: Link):
        self.links.append(link)

    def add_links(self, links: list):
        self.links.extend(links)

    def remove_link(self, link: Link):
        self.links.remove(link)

    def set_start(self, node: Node):
        self.start_node = node

    def _execute(self, **kwargs):
        if self.start_node is not None:
            self.start_node(**kwargs)
