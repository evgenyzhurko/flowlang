import PySide6

import io
from contextlib import redirect_stderr, redirect_stdout
from typing import Optional
from PySide6.QtQml import QmlElement
from PySide6.QtCore import QObject, Qt, Slot, Property, Signal
from .flow_vm import FlowVM

from .config import QML_IMPORT_NAME, QML_IMPORT_MAJOR_VERSION

@QmlElement
class FlowDebugVM(QObject):
    flowVMChanged = Signal()
    outputChanged = Signal()

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

        self._flow_vm = FlowVM()

        self._stdout = ''
        self._stderr = ''

    @Property(QObject, notify=flowVMChanged)
    def flow_vm(self):
        return self._flow_vm

    @flow_vm.setter
    def flow_vm(self, flow_vm):
        self._flow_vm = flow_vm
        self.flowVMChanged.emit()

    @Property(str, notify=outputChanged)
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, out):
        self._stdout = out
        self.outputChanged.emit()

    @Property(str, notify=outputChanged)
    def stderr(self):
        return self._stderr

    @stderr.setter
    def stderr(self, out):
        self._stderr = out
        self.outputChanged.emit()

    @Slot()
    def run(self):
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            self._flow_vm.flow()
        self._stdout = out.getvalue()
        self._stderr = err.getvalue()
        self.outputChanged.emit()

    @Slot()
    def clean_output(self):
        self._stdout = ''
        self._stderr = ''
        self.outputChanged.emit()
