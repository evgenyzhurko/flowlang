import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "./" as MyComponents

import flow.nodes

Rectangle {
    id: node
    
    property string uuid: ''
    property string name: ''
    property bool is_start_node: false
    property var input_pins: []
    property var output_pins: []

    signal requestDelete()
    signal setStartNode()
    signal removeInputLink(var paramName)
    signal removeOutputLink(var paramName)
    signal moveFinished()
    signal makeLink(var from, var fromParam, var to, var toParam)

    property bool node_hovered: false
    property bool move_started: false
    property var start_pos: Qt.point(0, 0)

    color: is_start_node ? "lightgreen" : "gray"
    border.width: 5
    border.color: node_hovered ? "red" : "blue"

    width: 150
    height: 100

    function update_object(delta_x, delta_y) {
        x += delta_x
        y += delta_y
    }

    MouseArea {
        anchors.fill: parent

        acceptedButtons: Qt.AllButtons
        hoverEnabled: true
        drag.target: node

        onClicked: (mouse) => {
            if (mouse.button === Qt.RightButton)
                contextMenu.popup()
        }

        onEntered: {
            node_hovered = true
        }

        onExited: {
            node_hovered = false
        }

        onReleased: (mouse) => {
            if (mouse.button === Qt.LeftButton)
                moveFinished()
        }
    }

    Menu {
        id: contextMenu

        MenuItem {
            text: "Delete Node"
            onTriggered: {
                requestDelete()
            }
        }
        
        MenuItem {
            text: "Set start"
            onTriggered: {
                setStartNode()
            }
        }
    }

    Column {
        anchors.fill: parent

        Text {
            text: node.name
            height: 40

            leftPadding: 5
            topPadding: 5
        }

        RowLayout {
            width: parent.width
            spacing: 0

            ColumnLayout {
                width: parent.width / 2
                Layout.alignment: Qt.AlignTop
                spacing: 0

                Repeater {
                    
                    width: node.width / 2
                    height: 60
                    model: node.input_pins
                    delegate: MyComponents.PinItem {
                        width: node.width / 2
                        height: 20
                        name: model.pin_name
                        node_uuid: uuid
                        pin_direction: 'in'

                        onDeleteAll: {
                            removeOutputLink(name)
                        }

                        onLinkRequested: (from, fromParam) => {
                            makeLink(from, fromParam, uuid, model.pin_name)
                        }
                    }
                }
            }

            ColumnLayout {
                width: parent.width / 2
                Layout.alignment: Qt.AlignTop
                spacing: 0
                
                Repeater {
                    Layout.alignment: Qt.AlignTop

                    width: node.width / 2
                    height: 60
                    model: node.output_pins
                    delegate: MyComponents.PinItem {
                        width: node.width / 2
                        height: 20
                        name: model.pin_name
                        is_editable: model.is_editable
                        value: model.pin_value
                        node_uuid: uuid
                        pin_direction: 'out'

                        onValueChanged: {
                            model.pin_value = value
                        }

                        onDeleteAll: {
                            removeInputLink(name)
                        }

                        onLinkRequested: (to, toParam) => {
                            makeLink(uuid, model.pin_name, to, toParam)
                        }
                    }
                }
            }
        }
    }
}