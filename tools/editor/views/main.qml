import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Shapes
import QtQuick.Dialogs

import "./" as MyComponents
import flow.nodes

ApplicationWindow {
    id: main
    width: 1000
    height: 600
    visible: true
    color: "white"

    FlowVM {
        id: flow_vm
    }

    NodeListVM {
        id: node_list_vm
        flow_vm: flow_vm
    }

    LinkListVM {
        id: link_list_vm
        flow_vm: flow_vm
    }

    FlowDebugVM {
        id: flow_debug_vm
        flow_vm: flow_vm
    }

    FileDialog {
        id: fileOpenDialog
        currentFolder: StandardPaths.standardLocations(StandardPaths.DocumentsLocation)[0]
        onAccepted: {
            flow_vm.load(selectedFile)
        }
    }

    FileDialog {
        id: fileSaveDialog
        defaultSuffix: 'json'
        fileMode: FileDialog.SaveFile
        currentFolder: StandardPaths.standardLocations(StandardPaths.DocumentsLocation)[0]
        onAccepted: {
            flow_vm.save(selectedFile)
        }
    }

    menuBar: MenuBar {

        Menu {
            title: "File"

            MenuItem {
                text: qsTr("New")
                onTriggered: flow_vm.reset()
            }

            MenuItem {
                text: qsTr("Load")
                onTriggered: fileOpenDialog.open()
            }

            MenuItem {
                text: qsTr("Save")
                onTriggered: fileSaveDialog.open()
            }

            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit();
            }
        }
        
        Menu {
            title: "Run"

            MenuItem {
                text: qsTr("Run")
                onTriggered: flow_debug_vm.run()
            }

            MenuItem {
                text: qsTr("Clean output")
                onTriggered: flow_debug_vm.clean_output()
            }
        }
    }

    Column {
        anchors.fill: parent

        SplitView {
            width: parent.width
            height: parent.height

            SplitView {
                orientation: Qt.Vertical
                SplitView.preferredWidth: parent.width * 0.8
                SplitView.preferredHeight: parent.height

                MyComponents.FlowView {
                    node_list_vm: node_list_vm
                    link_list_vm: link_list_vm

                    SplitView.preferredWidth: parent.width
                    SplitView.preferredHeight: parent.height * 0.8
                }

                Text {
                    text: flow_debug_vm.stdout + flow_debug_vm.stderr

                    SplitView.preferredWidth: parent.width
                    SplitView.preferredHeight: parent.height * 0.2
                }
            }

            MyComponents.Library {
                SplitView.preferredWidth: parent.width * 0.2
                SplitView.preferredHeight: parent.height

                onAddNode: (name) => {
                    node_list_vm.add_node(name)
                }
            }
        }
    }
}