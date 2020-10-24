import QtQuick 2.0
import QtQuick.Layouts 1.15

Item {
    id: root

    property int value: 50
    property int maxValue: 100
    property string text: ""

    Rectangle{
        height: root.height
        width: (root.width / root.maxValue) * root.value
        radius: root.height / 2
        color: "#0fb6df"
    }
}
