import PySide6

import io
from contextlib import redirect_stderr, redirect_stdout
from typing import Optional
from PySide6.QtQml import QmlElement
from PySide6.QtCore import Slot, QObject, Signal, QUrl
from flowlang import Flow

from .config import QML_IMPORT_NAME, QML_IMPORT_MAJOR_VERSION


@QmlElement
class FlowVM(QObject):
    flowChanged = Signal()

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

        self.flow = Flow()

    def set_flow(self, flow):
        self.flow = flow
        self.flowChanged.emit()

    @Slot()
    def reset(self):
        self.set_flow(Flow())

    @Slot(str)
    def save(self, path):
        with open(QUrl(path).toLocalFile(), 'w') as f:
            f.write(self.flow.to_json())

    @Slot(str)
    def load(self, path):
        with open(QUrl(path).toLocalFile(), 'r') as f:
            flow = Flow()
            flow.from_json(f.read())
            self.set_flow(flow)
