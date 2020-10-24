import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 1.4

Item {
    RowLayout{
        anchors.fill: parent
        anchors.margins: 10
        spacing: 20

        Text{
            text: "Title"
            color: "white"
            font.pixelSize: 16
        }

        Text{
            text: "Release Date"
            color: "white"
            font.pixelSize: 16
        }

        Text{
            text: "Rating"
            color: "white"
            font.pixelSize: 16
        }

        Rectangle{
            color: "black"
            Layout.fillHeight: true
            Layout.fillWidth: true
            radius: 10

            TextEdit{
                anchors.fill: parent
                anchors.leftMargin: 10
                verticalAlignment: Qt.AlignVCenter
                color: "white"
                font.pixelSize: 16

                selectByMouse: true
                selectionColor: "white"
                selectedTextColor: "black"
            }
        }
    }
}
