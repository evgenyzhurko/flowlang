import PySide6

from typing import Union, Any, Dict, Optional
from PySide6.QtQml import QmlElement
from PySide6.QtCore import QAbstractListModel, Qt, Slot, QObject, Signal, Property
from flowlang import Link, ExecutionLink

from .flow_vm import FlowVM

from .config import QML_IMPORT_NAME, QML_IMPORT_MAJOR_VERSION

@QmlElement
class LinkListVM(QAbstractListModel):
    SRC_X_ROLE = Qt.ItemDataRole.UserRole + 1
    SRC_Y_ROLE = Qt.ItemDataRole.UserRole + 2
    DST_X_ROLE = Qt.ItemDataRole.UserRole + 3
    DST_Y_ROLE = Qt.ItemDataRole.UserRole + 4

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
        return len(self._flow_vm.flow.links) if self._flow_vm is not None else 0

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None

        if index.row() > len(self._flow_vm.flow.links):
            return None

        link = self._flow_vm.flow.links[index.row()]
        if role == LinkListVM.SRC_X_ROLE:
            return link.source.x + 145
        elif role == LinkListVM.SRC_Y_ROLE:
            return link.source.y + 50 + 20 * (list(link.source.output_params.keys()).index(link.source_name))
        elif role == LinkListVM.DST_X_ROLE:
            return link.destination.x + 5
        elif role == LinkListVM.DST_Y_ROLE:
            return link.destination.y + 50 + 20 * (list(link.destination.input_params.keys()).index(link.destination_name))
        else:
            return None

    def roleNames(self) -> Dict[int, PySide6.QtCore.QByteArray]:
        roles = dict()
        roles[LinkListVM.SRC_X_ROLE] = b'src_x'
        roles[LinkListVM.SRC_Y_ROLE] = b'src_y'
        roles[LinkListVM.DST_X_ROLE] = b'dst_x'
        roles[LinkListVM.DST_Y_ROLE] = b'dst_y'
        return roles


    @Slot(str, str)
    def remove_input_links(self, uuid, name):
        self.beginResetModel()
        for link in self._flow_vm.flow.links:
            if str(link.source.uuid) == uuid and link.source_name == name:
                self._flow_vm.flow.links.remove(link)
        self.endResetModel()

    @Slot(str, str)
    def remove_output_links(self, uuid, name):
        self.beginResetModel()
        for link in self._flow_vm.flow.links:
            if str(link.destination.uuid) == uuid and link.destination_name == name:
                self._flow_vm.flow.links.remove(link)
        self.endResetModel()

    def get_node_by_id(self, uuid):
        for node in self._flow_vm.flow.nodes:
            if str(node.uuid) == uuid:
                return node
        return None

    @Slot(str, str, str, str)
    def make_link(self, src, srcParam, dst, dstParam):
        self.beginResetModel()
        for link in self._flow_vm.flow.links:
            if str(link.destination.uuid) == dst and link.destination_name == dstParam:
                self._flow_vm.flow.links.remove(link)
        
        src_node = self.get_node_by_id(src)
        dst_node = self.get_node_by_id(dst)
        if src_node.get_output_param(srcParam).callable and dst_node.get_input_param(dstParam).callable:
            self._flow_vm.flow.links.append(ExecutionLink(src_node, dst_node, source_exec=srcParam, destination_exec=dstParam))
        else:
            self._flow_vm.flow.links.append(Link(src_node, srcParam, dst_node, dstParam))
        
        self.endResetModel()

    @Slot(str)
    def delete_links(self, uuid):
        self.beginResetModel()
        self._flow_vm.flow.links = [
            link for link in self._flow_vm.flow.links if not (str(link.source.uuid) == uuid or str(link.destination.uuid) == uuid)]
        self.endResetModel()
