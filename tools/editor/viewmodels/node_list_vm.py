import PySide6

from typing import Union, Any, Dict, Optional
from PySide6.QtQml import QmlElement
from PySide6.QtCore import QAbstractListModel, Qt, Slot, QObject, Signal, Property
from flowlang import Library

from .flow_vm import FlowVM
from .pin_list_vm import InputPinListVM, OutputPinListVM

from .config import QML_IMPORT_NAME, QML_IMPORT_MAJOR_VERSION

@QmlElement
class NodeListVM(QAbstractListModel):
    NAME_ROLE = Qt.ItemDataRole.UserRole + 1
    UUID_ROLE = Qt.ItemDataRole.UserRole + 2
    POS_X_ROLE = Qt.ItemDataRole.UserRole + 3
    POS_Y_ROLE = Qt.ItemDataRole.UserRole + 4
    INPUT_PINS_ROLE = Qt.ItemDataRole.UserRole + 5
    OUTPUT_PINS_ROLE = Qt.ItemDataRole.UserRole + 6
    IS_START_NODE_ROLE = Qt.ItemDataRole.UserRole + 7

    flowVMChanged = Signal()

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

        self._flow_vm = FlowVM()
        self.flowVMChanged.connect(self.reset)

    @Property(QObject, notify=flowVMChanged)
    def flow_vm(self):
        return self._flow_vm

    @flow_vm.setter
    def flow_vm(self, flow_vm):
        self._flow_vm = flow_vm

        if self._flow_vm is not None:
            self._flow_vm.flowChanged.connect(self.reset)
            
        self.flowVMChanged.emit()

    @Slot()
    def reset(self):
        self.beginResetModel()
        self.endResetModel()

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._flow_vm.flow.nodes) if self._flow_vm is not None else 0

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None

        if index.row() > len(self._flow_vm.flow.nodes):
            return None

        node = self._flow_vm.flow.nodes[index.row()]
        if role == NodeListVM.NAME_ROLE:
            return node.get_class_name()
        if role == NodeListVM.UUID_ROLE:
            return str(node.uuid)
        elif role == NodeListVM.POS_X_ROLE:
            return node.x
        elif role == NodeListVM.POS_Y_ROLE:
            return node.y
        elif role == NodeListVM.INPUT_PINS_ROLE:
            return InputPinListVM(node)
        elif role == NodeListVM.OUTPUT_PINS_ROLE:
            return OutputPinListVM(node)
        elif role == NodeListVM.IS_START_NODE_ROLE:
            return self._flow_vm.flow.start_node == node
        else:
            return None

    def setData(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], value: Any, role: int = ...) -> bool:
        if not index.isValid():
            return None

        if index.row() > len(self._flow_vm.flow.nodes):
            return None

        node = self._flow_vm.flow.nodes[index.row()]
        if role == NodeListVM.POS_X_ROLE:
            node.x = value
        elif role == NodeListVM.POS_Y_ROLE:
            node.y = value
        else:
            return False
        return True

    def roleNames(self) -> Dict[int, PySide6.QtCore.QByteArray]:
        roles = dict()
        roles[NodeListVM.NAME_ROLE] = b'node_name'
        roles[NodeListVM.UUID_ROLE] = b'node_uuid'
        roles[NodeListVM.POS_X_ROLE] = b'node_x'
        roles[NodeListVM.POS_Y_ROLE] = b'node_y'
        roles[NodeListVM.INPUT_PINS_ROLE] = b'node_input_pins'
        roles[NodeListVM.OUTPUT_PINS_ROLE] = b'node_output_pins'
        roles[NodeListVM.IS_START_NODE_ROLE] = b'is_start_node'
        return roles

    @Slot(str)
    def delete_node(self, uuid):
        self.beginResetModel()
        for node in self._flow_vm.flow.nodes:
            if str(node.uuid) == uuid:
                self._flow_vm.flow.nodes.remove(node)
        self.endResetModel()

    @Slot(str)
    def set_start_node(self, uuid):
        self.beginResetModel()
        for node in self._flow_vm.flow.nodes:
            if str(node.uuid) == uuid:
                self._flow_vm.flow.set_start(node)
        self.endResetModel()

    @Slot(str)
    def add_node(self, node_name):
        if not Library().has_node(node_name):
            return

        self.beginResetModel()
        self._flow_vm.flow.add_node(Library().get_type(node_name)())
        self.endResetModel()