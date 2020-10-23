import QtQuick 2.13
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15

Item {
    state: MovieDetails.loading

    states: [
        State {
            name: "loading"
            PropertyChanges {
                target: loader
                visible: true
            }
        },

        State {
            name: "loaded"
            PropertyChanges {
                target: root_layout
                visible: true
            }
        }
    ]

    BusyIndicator {
        id: loader
        width: 200
        height: 200
        running: true
        anchors.centerIn: parent
        visible: false
    }


    // bg image
    Image {
        id: bgImage
        source: MovieDetails.backdrop
        width: root_layout.width
        height: detailLayout.height
        fillMode: Image.PreserveAspectCrop
        y: detailLayout.y
        visible: false
    }

    FastBlur {
        id: blur
        anchors.fill: bgImage
        source: bgImage
        radius: 32
        visible: false
    }

    Colorize {
        anchors.fill: bgImage
        source: blur
        saturation: 0.0
        visible: root_layout.visible
        opacity: 0.1
    }

    ColumnLayout {
        id: root_layout
        width: parent.width
        visible: false

        Button{
            id: backButton
            text: "Back"
            onClicked: root_item.state = ""
            Layout.alignment: Qt.AlignRight
        }

        RowLayout {
            id: detailLayout

            Image {
                source: MovieDetails.poster
            }

            ColumnLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop

                Text {
                    Layout.fillWidth: true
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    text: MovieDetails.title
                    font.pixelSize: 40
                    color: "White"
                }

                Row{
                    opacity: 0.7
                    spacing: 5

                    Text {
                        Layout.fillWidth: true
                        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                        text: "("+ MovieDetails.release_date + ")"
                        color: "White"
                    }

                    Text {
                        Layout.fillWidth: true
                        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                        text: MovieDetails.genres
                        color: "White"
                    }

                    Text {
                        Layout.fillWidth: true
                        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                        text: "language: " + MovieDetails.language
                        color: "White"
                    }

                    Text {
                        Layout.fillWidth: true
                        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                        text: "runtime: " + MovieDetails.runtime + " min."
                        color: "White"
                    }
                }

                Text {
                    Layout.fillWidth: true
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    text: MovieDetails.tagline
                    font.pixelSize: 18
                    color: "White"
                    opacity: 0.7
                    leftPadding: 50
                }

                Text {
                    Layout.fillWidth: true
                    text: MovieDetails.overview
                    color: "White"
                    font.pixelSize: 16
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    leftPadding: 50
                }
            }
        }
    }
}
