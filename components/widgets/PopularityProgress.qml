import QtQuick 2.0

Rectangle {
    id: root
    width: 50
    height: 50
    color: "#141414"
    radius: width

    property int percentage: 25

    Canvas {
        id: canvas
        width: root.width
        height: root.height

        onPaint: {
            var ctx = getContext("2d");
            ctx.reset();

            var radiant = root.percentage * 0.062831853071796

            ctx.beginPath();
            ctx.fillStyle = "lightgreen";

            var centerX = width / 2;
            var centerY = height / 2;
            var radius = width / 2;

            ctx.arc(centerX, centerY, radius, 0, radiant, false);

            ctx.lineTo(centerX, centerY);
            ctx.fill();
        }

        rotation: -90
    }

    Rectangle{
        color: root.color
        width: root.width - 10
        height: root.height - 10
        anchors.centerIn: parent
        radius: width

        Item{
            width: childrenRect.width
            height: childrenRect.height
            anchors.centerIn: parent

            Text{
                id: popularityText
                text: root.percentage
                color: "white"
                font.bold: true
                font.pixelSize: 18
            }

            Text{
                text: "%"
                color: "white"
                font.bold: true
                font.pixelSize: 10
                anchors.left: popularityText.right
                anchors.top: popularityText.top
            }
        }
    }
}
