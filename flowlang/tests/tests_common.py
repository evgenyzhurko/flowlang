import time
import unittest
from numpy import mean

from .. import Variable, ExecutionLink, Link, Flow
from .. import ForNode, IncrementNode, PrintNode


def make_increment_flow():
    node1 = IncrementNode()
    node2 = IncrementNode()
    node3 = IncrementNode()
    node4 = IncrementNode()
    node5 = IncrementNode()

    execution1 = ExecutionLink(node1, node2)
    execution2 = ExecutionLink(node2, node3)
    execution3 = ExecutionLink(node3, node4)
    execution4 = ExecutionLink(node4, node5)

    link12 = Link(node1, 'value', node2, 'value')
    link23 = Link(node2, 'value', node3, 'value')
    link34 = Link(node3, 'value', node4, 'value')
    link45 = Link(node4, 'value', node5, 'value')

    flow = Flow()
    flow.set_start(node1)
    flow.add_nodes([node1, node2, node3, node4, node5])
    flow.add_links([link12, link23, link34, link45, execution1, execution2, execution3, execution4])

    return flow

def make_iterable_flow():
    node1 = PrintNode()
    node2 = ForNode()
    node3 = PrintNode()
    node4 = PrintNode()

    node1.input_values['msg'].set_value('Started...')
    node4.input_values['msg'].set_value('Finished...')
    node2.input_values['end'].set_value(3)

    execution1 = ExecutionLink(node1, node2)
    execution2 = ExecutionLink(node2, node3)
    execution3 = ExecutionLink(node2, node4, source_exec='finally')

    link23 = Link(node2, 'index', node3, 'msg')

    flow = Flow()
    flow.set_start(node1)
    flow.add_nodes([node1, node2, node3])
    flow.add_links([execution1, execution2, execution3, link23])

    return flow

class TestBasicFlows(unittest.TestCase):
    def test_increment_flow(self):
        flow = make_increment_flow()

        for i in range(3):
            var = Variable(float, i+1)
            flow.start_node.set_input_value('value', var)
            flow()

    def test_for_flow(self):
        flow = make_increment_flow()
        timings_flow = []
        for i in range(100):
            start = time.perf_counter()
            flow()
            timings_flow.append(time.perf_counter() - start)
        
        
        timings = []
        for i in range(100):
            start = time.perf_counter()
            a = 0
            for i in range(5):
                a += 1 + i
            timings.append(time.perf_counter() - start)
        print(f'Execution timings: {mean(timings_flow)} {mean(timings)}')
