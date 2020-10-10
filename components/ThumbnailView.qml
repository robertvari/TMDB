import QtQuick 2.0
import "widgets"

Item{

    ListModel {
        id: contactModel

        ListElement {
            original_title: "Bill Smith"
            poster: "555 3264"
            rating: "Budapest"
            release_date: "1998 aug 23."
        }
    }

    GridView {
        id: dataListView
        anchors.fill: parent
        cellWidth: 260
        cellHeight: 350

        model: contactModel

        delegate: Rectangle {
            width: dataListView.cellWidth - 10
            height: dataListView.cellHeight - 10
            color: "gray"

            Text {
                text: name + " " + number + " " + address
            }
        }
    }
}


