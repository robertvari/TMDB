import QtQuick 2.0
import "widgets"

Item {

    Rectangle{
        color: "lightblue"
        anchors.fill: parent

        IconButton{
            icon: ResourceLoader.get_resource('arrow-alt-circle-left.svg')
            onClicked: root_item.state = ""
        }
    }
}
