import QtQuick 2.13
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {

    ColumnLayout{
        width: parent.width

        Button{
            text: "Back"
            onClicked: root_item.state = ""
            Layout.alignment: Qt.AlignRight
        }

        RowLayout{
            Layout.fillWidth: True

            Image {
                source: MovieDetails.poster
            }

            ColumnLayout{
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop

                Text {
                    Layout.fillWidth: true
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    text: MovieDetails.title
                    font.pixelSize: 30
                    color: "White"
                }

                Text {
                    Layout.fillWidth: true
                    text: MovieDetails.overview
                    color: "White"
                    font.pixelSize: 16
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                }
            }
        }
    }
}
