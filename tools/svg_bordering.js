function fromSymKey(key) {
    code = 0x100000 - 0x10000 + ((parseInt(key.slice(1, 4), 16) - 256) * 96) + ((parseInt(key.slice(4, 5), 16)) * 16) + parseInt(key.slice(5, 6), 16) + 1
    return String.fromCharCode(0xD800 + (code >> 10), 0xDC00 + (code & 0x3FF));
}

function drawGrid(key) {
    var zoom = 10;
    var cnv = document.getElementById(key);

    var gridOptions = {
        minorLines: {
            separation: zoom,
            color: '#00FF00'
        },
        majorLines: {
            separation: zoom * 10,
            color: '#FF0000'
        }
    };

    drawGridLines(cnv, gridOptions.minorLines);
    drawGridLines(cnv, gridOptions.majorLines);
    var context = cnv.getContext("2d");
    //line
    context.font = (30 * zoom) + "px 'SignWriting 2010'";
    context.fillStyle = "black";
    context.fillText(fromSymKey(key), (zoom * 10), (zoom * 10));

    return;
}

function drawGridLines(cnv, lineOptions) {


    var iWidth = cnv.width;
    var iHeight = cnv.height;

    var ctx = cnv.getContext('2d');

    ctx.strokeStyle = lineOptions.color;
    ctx.strokeWidth = 1;

    ctx.beginPath();

    var iCount = null;
    var i = null;
    var x = null;
    var y = null;

    iCount = Math.floor(iWidth / lineOptions.separation);

    for (i = 1; i <= iCount; i++) {
        x = (i * lineOptions.separation);
        ctx.moveTo(x, 0);
        ctx.lineTo(x, iHeight);
        ctx.stroke();
    }


    iCount = Math.floor(iHeight / lineOptions.separation);

    for (i = 1; i <= iCount; i++) {
        y = (i * lineOptions.separation);
        ctx.moveTo(0, y);
        ctx.lineTo(iWidth, y);
        ctx.stroke();
    }

    ctx.closePath();

    return;
}
