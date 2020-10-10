import QtQuick 2.0
import QtQuick.Layouts 1.15
import "widgets"

Rectangle {
    id: root
    color: "black"

    ColumnLayout{
        width: root.width

        Image{
            id: logo
            Layout.alignment: Qt.AlignHCenter
            Layout.maximumWidth: parent.width - 10
            source: "../images/logo.png"
            fillMode: Image.PreserveAspectFit
        }

        MenuItem{
            title: "Movies"
            Layout.fillWidth: true
        }

        MenuItem{
            title: "TV Shows"
            Layout.fillWidth: true
        }

        MenuItem{
            title: "People"
            Layout.fillWidth: true
        }
    }
}
