import QtQuick 2.0

Item {
    id: root
    property string icon
    property int size: 30
    signal clicked

    width: size
    height: size

    Image{
        source: icon
        anchors.fill: parent
        sourceSize: Qt.size(size, size)
        fillMode: Image.PreserveAspectFit
    }

    MouseArea{
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: root.clicked()
    }
}
