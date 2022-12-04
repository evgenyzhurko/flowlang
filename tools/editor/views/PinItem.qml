import QtQuick
import QtQuick.Controls

import flow.nodes

Rectangle {
    id: pin

    property string name: ''
    property string node_uuid: ''
    property string value: ''
    property bool is_editable: false
    property bool pin_hovered: false
    property var pin_direction

    signal deleteAll()
    signal linkRequested(var uuid, var name)

    color: is_editable ? "lightgray" : "gray"
    border.width: 1
    border.color: pin_hovered ? "red" : "blue"

    Text {
        anchors.fill: parent
        text: pin.name
        visible: !is_editable
        leftPadding: 15
    }

    TextInput {
        id: text_input
        text: pin.value
        anchors.fill: parent
        visible: is_editable
        clip: true

        onAccepted: {
            focus = false
            pin.value = text
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent

        acceptedButtons: Qt.AllButtons
        hoverEnabled: true
        drag.target: draggable

        onClicked: (mouse) => {
            if (mouse.button === Qt.RightButton) {
                contextMenu.popup()
            }
            else {
                text_input.forceActiveFocus()
            }
        }

        onEntered: {
            pin_hovered = true
        }

        onExited: {
            pin_hovered = false
        }
    }

    Item {
        id: draggable
        Drag.active: mouseArea.drag.active
        Drag.hotSpot.x: 0
        Drag.hotSpot.y: 0
        Drag.mimeData: { 
            'node': node_uuid,
            'var': name,
            'direction': pin_direction
        }
        Drag.dragType: Drag.Automatic
    }

    DropArea {
        anchors.fill: parent
        onEntered: {
            pin_hovered = true
        }

        onDropped: (drop) => {
            if (drop.keys.includes('node') && drop.keys.includes('var') && drop.keys.includes('direction')) {
                if ((drop.getDataAsString('direction') === pin_direction) ||
                    (drop.getDataAsString('node') === node_uuid)) {
                    drop.accepted = false
                }
                else {
                    drop.accept()
                    linkRequested(drop.getDataAsString('node'), drop.getDataAsString('var'))
                }
            }
            pin_hovered = false
        }

        onExited: {
            pin_hovered = false
        }
    }
    
    Menu {
        id: contextMenu
        MenuItem {
            text: "Delete Connections"

            onTriggered: {
                deleteAll()
            }
        }
    }
}