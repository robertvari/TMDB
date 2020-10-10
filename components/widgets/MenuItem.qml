import QtQuick 2.0

Rectangle {
    id: root
    color: "lightgray"
    height: titleText.height + 5

    property string title: "Item Title"


    Text {
        id: titleText
        text: title
        font.pixelSize: 30
        anchors.centerIn: parent
    }
}
