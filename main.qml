import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
import "./components"

Window {
    id: window
    width: 1200
    height: 800
    visible: true
    title: qsTr("TMDB")
    color: "#141414"

    Item{
        anchors.fill: parent
        id: root_item

        states: [
            State {
                name: "details"
                PropertyChanges {
                    target: thumbViewLayout
                    visible: false
                }

                PropertyChanges {
                    target: detailsView
                    visible: true
                }
            }
        ]

        RowLayout{
            id: thumbViewLayout
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
