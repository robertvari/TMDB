import QtQuick 2.0

Rectangle {
    id: root
    color: "transparent"

    height: titleText.height + 5

    property string title: "Item Title"
    signal clicked

    states: [
        State {
            name: "hovered"
            PropertyChanges {
                target: titleText
                color: "#141414"
            }

            PropertyChanges {
                target: root
                color: "#99aab5"
            }
        },

        State {
            name: "pressed"
            PropertyChanges {
                target: titleText
                color: "#141414"
            }

            PropertyChanges {
                target: root
                color: "lightgreen"
            }
        }
    ]

    Text {
        id: titleText
        text: title
        font.pixelSize: 20
        anchors.centerIn: parent
        color: "#99aab5"
    }

    MouseArea{
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        hoverEnabled: true

        onEntered: root.state = "hovered"
        onExited: root.state = ""
        onPressed: root.state = "pressed"
        onReleased: root.state = "hovered"

        onClicked: root.clicked()
    }
}
