import QtQuick 2.15
import QtQuick.Layouts 1.15
import "widgets"

Item{

    ListModel {
        id: contactModel

        ListElement {
            movie_id: 348
            original_title: "Alien"
            poster_path: "../images/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg"
            popularity: 45.92
            release_date: "1979-05-25"
        }

        ListElement {
            movie_id: 126889
            original_title: "Alien: Covenant"
            poster_path: "../images/zecMELPbU5YMQpC81Z8ImaaXuf9.jpg"
            popularity: 58.604
            release_date: "2017-05-09"
        }

        ListElement {
            movie_id: 593035
            original_title: "Alien Warfare"
            poster_path: "../images/rJOj0T5DyChfECevDg0xpEGznsl.jpg"
            popularity: 35.354
            release_date: "2019-04-05"
        }
    }

    GridView {
        id: dataListView
        anchors.fill: parent
        cellWidth: 184
        cellHeight: 377

        model: contactModel

        delegate: Rectangle {
            id: movieItemRect
            width: dataListView.cellWidth - 10
            height: dataListView.cellHeight - 10
            color: "transparent"

            states: [
                State {
                    name: "hovered"
                    PropertyChanges {
                        target: movieItemRect
                        color: "#444444"
                    }
                }
            ]

            transitions: Transition {
                ColorAnimation { duration: 200 }
            }

            // layout
            ColumnLayout{
                anchors.fill: parent

                // poster
                Image{
                    Layout.fillWidth: true
                    Layout.maximumHeight: dataListView.cellHeight - 100
                    Layout.minimumHeight: dataListView.cellHeight - 100
                    source: poster_path
                    fillMode: Image.PreserveAspectFit
                }

                // Movie title and release date
                Rectangle{
                    id: itemTitleRect
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "transparent"

                    ColumnLayout{
                        width: itemTitleRect.width

                        Label{
                            text: original_title
                            font.pixelSize: 20
                        }

                        Label{
                            text: release_date
                        }

                        Label{
                            text: popularity
                        }
                    }
                }
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true

                onEntered: movieItemRect.state = "hovered"
                onExited: movieItemRect.state = ""
            }
        }
    }
}


