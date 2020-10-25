import QtQuick 2.0
import QtQuick.Layouts 1.15
import "widgets"

Item {
    ColumnLayout{
        width: parent.width

        Item{
            id: detailsMenu
            Layout.fillWidth: true
            implicitHeight: 40

            IconButton{
                id: icon1
                icon: ResourceLoader.get_resource('arrow-alt-circle-left.svg')
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.margins: 20

                onClicked: root_item.state = ""
            }
        }

        Rectangle{
            Layout.fillWidth: true
            implicitHeight: moviePoster.height + 40
            color: "gray"

            RowLayout {
                id: posterLayout
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.margins: 20

                Image {
                    sourceSize: Qt.size(300, 450)
                    source: MovieDetail.poster
                }

                ColumnLayout{
                    Layout.fillWidth: true

                    Text{
                        text: "2067 (2020)"
                        font.pixelSize: 30
                        color: "white"
                    }

                    Text{
                        text: "2020 january 12 | Science Fiction, Thriller, Drama | 1h 54m"
                        font.pixelSize: 16
                        color: "white"
                    }

                    Text{
                        text: "The fight for the future has begun."
                        font.pixelSize: 16
                        color: "white"
                    }

                    Text{
                        text: "Overview"
                        font.pixelSize: 20
                        font.bold: true
                        color: "white"
                    }

                    Text{
                        text: "A lowly utility worker is called to the future by..."
                        font.pixelSize: 16
                        color: "white"
                    }
                }
            }
        }
    }
}
