import os
import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine


from viewmodels.flow_vm import FlowVM
from viewmodels.library_list_vm import LibraryListVM
from viewmodels.link_list_vm import LinkListVM
from viewmodels.node_list_vm import NodeListVM
from viewmodels.pin_list_vm import InputPinListVM, OutputPinListVM
from viewmodels.flow_debug_vm import FlowDebugVM


QML_IMPORT_NAME = "flow.nodes"
QML_IMPORT_MAJOR_VERSION = 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(created)f - %(message)s')

    app = QApplication()
    engine = QQmlApplicationEngine()
    engine.load(os.path.dirname(__file__) + '/views/main.qml')

    sys.exit(app.exec())