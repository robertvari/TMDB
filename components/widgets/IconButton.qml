import QtQuick 2.0
import QtGraphicalEffects 1.12

Item {
    id: root
    property string icon
    property int size: 30
    property color iconColor: "white"
    signal clicked

    width: size
    height: size

    Image{
        id: iconImage
        source: icon
        anchors.fill: parent
        sourceSize: Qt.size(size, size)
        fillMode: Image.PreserveAspectFit
        visible: false
    }

    ColorOverlay {
        id: colorOverlay
        anchors.fill: iconImage
        source: iconImage
        color: root.iconColor
    }

    MouseArea{
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: root.clicked()
    }
}
