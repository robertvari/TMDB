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
            state: MovieListProxy.sort_mode === "title"? "active": ""
            onClicked: MovieListProxy.sort_mode = "title"
            direction: MovieListProxy.sort_direction? "up":"down"
        }

        FilterButton{
            text: "Release Date"
            state: MovieListProxy.sort_mode === 'sort_date'? "active": ""
            onClicked: MovieListProxy.sort_mode = "sort_date"
            direction: MovieListProxy.sort_direction? "up":"down"
        }

        FilterButton{
            text: "Rating"
            state: MovieListProxy.sort_mode === 'vote_average'? "active": ""
            onClicked: MovieListProxy.sort_mode = "vote_average"
            direction: MovieListProxy.sort_direction? "up":"down"
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
