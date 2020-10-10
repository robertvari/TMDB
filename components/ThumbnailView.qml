import QtQuick 2.0
import "widgets"

Item{

    ListModel {
        id: contactModel

        ListElement {
            movie_id: 348
            original_title: "Alien"
            poster_path: "https://image.tmdb.org/t/p/w300/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg"
            popularity: 45.92
            release_date: "1979-05-25"
        }

        ListElement {
            movie_id: 126889
            original_title: "Alien: Covenant"
            poster_path: "https://image.tmdb.org/t/p/w300/zecMELPbU5YMQpC81Z8ImaaXuf9.jpg"
            popularity: 58.604
            release_date: "2017-05-09"
        }

        ListElement {
            movie_id: 593035
            original_title: "Alien Warfare"
            poster_path: "https://image.tmdb.org/t/p/w300/rJOj0T5DyChfECevDg0xpEGznsl.jpg"
            popularity: 35.354
            release_date: "2019-04-05"
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


