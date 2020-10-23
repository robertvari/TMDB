import QtQuick 2.15
import QtQuick.Layouts 1.15
import "widgets"

Item{
    ColumnLayout{
        anchors.fill: parent

        Progressbar{
            Layout.fillWidth: true
            implicitHeight: 20
            visible: MovieList.show_progress
            maxValue: MovieList.max_job_count
            value: MovieList.progress_value
        }

        GridView {
        id: dataListView
        Layout.fillHeight: true
        Layout.fillWidth: true
        cellWidth: 184
        cellHeight: 377
        clip: true

        model: MovieList

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
                    Layout.alignment: Qt.AlignTop

                    source: movie_item.poster_path
                    fillMode: Image.PreserveAspectFit

                    PopularityProgress{
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.margins: 10

                        percentage: movie_item.vote_average
                    }
                }

                // Movie title and release date
                Rectangle{
                    id: itemTitleRect
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "transparent"

                    ColumnLayout{
                        anchors.left: itemTitleRect.left
                        anchors.right: itemTitleRect.right
                        anchors.top: itemTitleRect.top
                        anchors.margins: 5

                        Label{
                            Layout.fillWidth: true
                            text: movie_item.title
                            font.pixelSize: 20
                            wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                            width: parent.width
                        }

                        Label{
                            text: movie_item.release_date
                            opacity: 0.5
                            font.pixelSize: 12
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

                onClicked: {
                    MovieDetails.load(movie_item.id)
                    root_item.state = "details"
                }
            }
        }
    }

    }
}


