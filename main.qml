import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
import "components"

Window {
    width: 1200
    height: 800
    visible: true
    title: qsTr("TMDB")
    color: "#141414"

    Item {
        id: root_item
        anchors.fill: parent

        states: [
            State {
                name: "details"
                PropertyChanges {
                    target: thumbnailViewLayout
                    visible: false
                }

                PropertyChanges {
                    target: detailsView
                    visible: true
                }
            }
        ]

        RowLayout{
            id: thumbnailViewLayout
            anchors.fill: parent

            Menu{
                property int size: 200
                Layout.fillHeight: true
                Layout.minimumWidth: size
                Layout.maximumWidth: size
            }

            ThumbnailView{
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }

        DetailsView{
            id: detailsView
            anchors.fill: parent
            visible: false
        }
    }
}
