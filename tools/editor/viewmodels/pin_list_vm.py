import PySide6
from enum import Enum
from typing import Union, Any, Dict, Optional
from PySide6.QtQml import QmlElement
from PySide6.QtCore import QAbstractListModel, Qt, QObject, QEnum
from flowlang import Node

from .config import QML_IMPORT_NAME, QML_IMPORT_MAJOR_VERSION

@QmlElement
class InputPinListVM(QAbstractListModel):
    PIN_NAME_ROLE = Qt.ItemDataRole.UserRole + 1

    def __init__(self, node: Node, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

        self.node = node

    def reset(self):
        self.beginResetModel()
        self.endResetModel()

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.node.input_params)

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None

        if index.row() > len(self.node.input_params):
            return None

        param = list(self.node.input_params.items())[index.row()]
        if role == InputPinListVM.PIN_NAME_ROLE:
            return param[0]
        else:
            return None

    def roleNames(self) -> Dict[int, PySide6.QtCore.QByteArray]:
        roles = dict()
        roles[InputPinListVM.PIN_NAME_ROLE] = b'pin_name'
        return roles

@QmlElement
class OutputPinListVM(QAbstractListModel):
    PIN_NAME_ROLE = Qt.ItemDataRole.UserRole + 1
    IS_EDITABLE_PIN_ROLE = Qt.ItemDataRole.UserRole + 2
    PIN_VALUE_ROLE = Qt.ItemDataRole.UserRole + 3

    def __init__(self, node: Node, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

        self.node = node

    def reset(self):
        self.beginResetModel()
        self.endResetModel()

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.node.output_params)

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None

        if index.row() > len(self.node.output_params):
            return None

        param = list(self.node.output_params.items())[index.row()]
        param_value = list(self.node.output_values.items())[index.row()]
        if role == OutputPinListVM.PIN_NAME_ROLE:
            return param[0]
        elif role == OutputPinListVM.IS_EDITABLE_PIN_ROLE:
            return param[1].editable
        elif role == OutputPinListVM.PIN_VALUE_ROLE:
            return param_value[1].get_value() if param[1].editable else ''
        else:
            return None

    def setData(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], value: Any, role: int = ...) -> bool:
        if not index.isValid():
            return None

        if index.row() > len(self.node.output_params):
            return None

        param = list(self.node.output_params.items())[index.row()]
        param_value = list(self.node.output_values.items())[index.row()]
        if role == OutputPinListVM.PIN_VALUE_ROLE:
            param[1].default_value = param[1].dtype(value)
            param_value[1].default_value = param[1].dtype(value)
            param_value[1].set_value(param[1].default_value)
        
        return super().setData(index, value, role)

    def roleNames(self) -> Dict[int, PySide6.QtCore.QByteArray]:
        roles = dict()
        roles[OutputPinListVM.PIN_NAME_ROLE] = b'pin_name'
        roles[OutputPinListVM.IS_EDITABLE_PIN_ROLE] = b'is_editable'
        roles[OutputPinListVM.PIN_VALUE_ROLE] = b'pin_value'
        return roles