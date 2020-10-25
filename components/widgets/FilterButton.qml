import QtQuick 2.0

Text {
    id: root
    font.pixelSize: 16
    color: "white"
    opacity: 0.6

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

    MouseArea{
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked()
    }
}
