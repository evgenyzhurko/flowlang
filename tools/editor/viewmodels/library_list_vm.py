import PySide6

from enum import Enum
import logging
from typing import Union, Any, Dict, Optional
from PySide6.QtQml import QmlElement
from PySide6.QtCore import QAbstractListModel, Qt
from flowlang import Library

from .config import QML_IMPORT_NAME, QML_IMPORT_MAJOR_VERSION

@QmlElement
class LibraryListVM(QAbstractListModel):
    NODE_NAME_ROLE = Qt.ItemDataRole.UserRole + 1
    NODE_PATH_ROLE = Qt.ItemDataRole.UserRole + 2

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(Library().nodes)

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if not index.isValid():
            return None

        if index.row() > len(Library().nodes):
            return None

        if role == LibraryListVM.NODE_NAME_ROLE:
            return list(Library().nodes.items())[index.row()][0].split('.')[-1]
        elif role == LibraryListVM.NODE_PATH_ROLE:
            return list(Library().nodes.items())[index.row()][0]
        else:
            return None

    def roleNames(self) -> Dict[int, PySide6.QtCore.QByteArray]:
        roles = dict()
        roles[LibraryListVM.NODE_NAME_ROLE] = b'node_name'
        roles[LibraryListVM.NODE_PATH_ROLE] = b'node_path'
        return roles