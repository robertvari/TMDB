import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import "widgets"

Item {
    state: MovieDetail.loading

    states: [
        State {
            name: "loading"
            PropertyChanges {
                target: movieDetailsContainer
                visible: false
            }

            PropertyChanges {
                target: loaderIndicator
                visible: true
            }
        },

        State {
            name: "loaded"
            PropertyChanges {
                target: movieDetailsContainer
                visible: true
            }

            PropertyChanges {
                target: loaderIndicator
                visible: false
            }
        }
    ]

    BusyIndicator{
        id: loaderIndicator
        implicitWidth: 200
        implicitHeight: 200
        visible: false
        running: true
        anchors.centerIn: parent
    }

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
            id: movieDetailsContainer
            Layout.fillWidth: true
            implicitHeight: moviePoster.height + 40
            color: "gray"
            visible: true

            RowLayout {
                id: posterLayout
                anchors.fill: parent
                anchors.margins: 20

                Image {
                    id: moviePoster
                    sourceSize: Qt.size(300, 450)
                    source: MovieDetail.poster
                }

                ColumnLayout{
                    Layout.fillWidth: true

                    Text{
                        text: MovieDetail.title
                        font.pixelSize: 30
                        color: "white"
                        Layout.fillWidth: true
                        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    }

                    Text {
                        text: MovieDetail.date +" | " + MovieDetail.genres + " | " + MovieDetail.runtime
                        font.pixelSize: 16
                        color: "white"
                    }

                    Text{
                        text: MovieDetail.tagline
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
                        text: MovieDetail.overview
                        font.pixelSize: 16
                        color: "white"
                        Layout.fillWidth: true
                        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    }
                }
            }
        }
    }
}
