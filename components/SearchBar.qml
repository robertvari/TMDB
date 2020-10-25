import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 1.4
import "widgets"

Item {

    RowLayout{
        anchors.fill: parent
        anchors.margins: 10
        spacing: 20

        FilterButton{
            text: "Title"
            state: MovieListProxy.sort_mode === "title"? "active": null

            onClicked: MovieListProxy.sort_mode = "title"
        }

        FilterButton{
            text: "Release Date"
            state: MovieListProxy.sort_mode === "date_sorting"? "active": null

            onClicked: MovieListProxy.sort_mode = 'date_sorting'
        }

        FilterButton{
            text: "Rating"
            state: MovieListProxy.sort_mode === "vote_average"? "active": null

            onClicked: MovieListProxy.sort_mode = 'vote_average'
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

                onTextChanged: MovieListProxy.set_filter(text)
            }
        }
    }
}
