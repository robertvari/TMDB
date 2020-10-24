import QtQuick 2.0
import QtGraphicalEffects 1.15

Text {
    id: root
    font.pixelSize: 16
    color: "white"
    opacity: 0.6

    property string direction: "down"

    signal clicked

    states: [
        State {
            name: "active"
            PropertyChanges {
                target: root
                opacity: 1
            }
        }
    ]

    transitions: Transition {
        NumberAnimation {
            properties: "opacity";
            duration: 100
            }
    }

    Image{
        id: icon
        source: "../../images/arrow-up.svg"
        sourceSize: Qt.size(12, 12)
        visible: false
        anchors.left: root.right
        anchors.verticalCenter: root.verticalCenter
        anchors.margins: 2
    }

    ColorOverlay {
        anchors.fill: icon
        source: icon
        color: root.color
        opacity: 1
        visible: root.state === "active"? true:false
        rotation: root.direction === "up"? 0: 180
    }

    MouseArea{
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: root.clicked()
    }
}
