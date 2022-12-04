import QtQuick
import QtQuick.Controls
import QtQuick.Shapes

import "./" as MyComponents
import flow.nodes

ScrollView {
    id: root

    property var link_list_vm
    property var node_list_vm

    clip: true

    Item {
        id: flow_item

        signal nodeChanged()

        function update_root() {
            root.contentWidth = flow_item.childrenRect.width
            root.contentHeight = flow_item.childrenRect.height
        }

        Repeater {
            id: node_list_view
            anchors.fill: parent
            model: root.node_list_vm
            delegate: MyComponents.NodeItem {
                name: model.node_name
                uuid: model.node_uuid
                input_pins: model.node_input_pins
                output_pins: model.node_output_pins
                is_start_node: model.is_start_node
                x: model.node_x
                y: model.node_y
                onXChanged: {
                    model.node_x = x
                    flow_item.nodeChanged()
                }
                onYChanged: {
                    model.node_y = y
                    flow_item.nodeChanged()
                }
                onMoveFinished: {
                    flow_item.update_root()
                }
                onRemoveInputLink: (paramName) => {
                    link_list_vm.remove_input_links(uuid, paramName)
                }
                onRemoveOutputLink: (paramName) => {
                    link_list_vm.remove_output_links(uuid, paramName)
                }
                onRequestDelete: () => {
                    link_list_vm.delete_links(model.node_uuid)
                    node_list_vm.delete_node(model.node_uuid)
                }
                onMakeLink: (from, fromParam, to, toParam) => {
                    link_list_vm.make_link(from, fromParam, to, toParam)
                }
                onSetStartNode: {
                    node_list_vm.set_start_node(uuid)
                }
                Component.onCompleted: {
                    flow_item.update_root()
                }
            }
        }

        Repeater {
            id: link_item
            model: root.link_list_vm
            delegate: Shape {
                id: shape
                containsMode: Shape.FillContains
                ShapePath {
                    fillColor: "transparent"
                    strokeWidth: 4
                    strokeColor: model.hovered ? "red" : "green"
                    strokeStyle: ShapePath.DashLine
                    dashPattern: [ 1, 0 ]
                    startX: model.src_x; startY: model.src_y

                    PathCubic {
                        x: model.dst_x
                        y: model.dst_y

                        control1X: model.src_x + (model.dst_x - model.src_x) * 0.45
                        control1Y: model.src_y
                        control2X: model.src_x + (model.dst_x - model.src_x) * 0.55
                        control2Y: model.dst_y
                    }
                }
            }
        }

        Connections {
            target: flow_item
            function onNodeChanged() {
                link_item.model.reset()
            }
        }
    }
}