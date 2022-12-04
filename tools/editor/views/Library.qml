import QtQuick
import QtQuick.Controls

import flow.nodes

ListView {
    id: list_view
    width: parent.width * 0.2
    height: parent.height

    signal addNode(var name)

    model: LibraryListVM {}

    delegate: Rectangle {
        width: parent.width
        height: 20
        color: index % 2 == 0 ? 'gray' : 'lightgray'

        Text {
            text: node_name
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.AllButtons

            onClicked: (mouse) => {
                if (mouse.button === Qt.RightButton)
                    contextMenu.popup()
            }
        }

        Menu {
            id: contextMenu
            MenuItem {
                text: "Add"

                onTriggered: {
                    addNode(node_path)
                }
            }
        }
    }
}