import QtQuick 2.13
import QtQuick.Layouts 1.15

Item {
    id: root

    property int value: 50
    property int maxValue: 100
    property string text: ""

    Rectangle{
        id: progressRect
        height: parent.height - 6
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.margins: 3
        width: (parent.width / maxValue) * value
        radius: 8
        color: "#0fb6df"
        clip: true
    }

    Text{
        id: progressText
        text: root.text
        anchors.centerIn: parent
        font.pixelSize: 16
        color: "white"
    }
}
