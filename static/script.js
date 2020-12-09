function updateUI() {
    colorUno = document.getElementById("vendedorUnoColor");
    colorDos = document.getElementById("vendedorDosColor");
    for (j = 0; j < colorUno.length; j++) {
        colorUno.options[j].disabled = false;
        colorDos.options[j].disabled = false;
    }
    for (i = 0; i < colorUno.length; i++) {
        if (colorUno.options[i].selected) {
            colorDos.options[i].disabled = true
            colorDos.options[i].selected = false
        }
        if (colorDos.options[i].selected) {
            colorUno.options[i].disabled = true;
            colorUno.options[i].selected = false;
        }
    }
}

function download() {
    html2canvas(document.querySelector('#mapWrapper')).then(canvas => {
        var dt = canvas.toDataURL('image/png');
        dt = dt.replace(/^data:image\/[^;]*/, 'data:application/octet-stream');
        dt = dt.replace(/^data:application\/octet-stream/, 'data:application/octet-stream;headers=Content-Disposition%3A%20attachment%3B%20filename=Canvas.png');
        var download = document.createElement('a');
        var label = document.createTextNode("Descargar");
        download.appendChild(label);
        download.title = "Descargar";
        download.href = dt;
        var downloadWrapper = document.querySelector("#downloadWrapper")
        downloadWrapper.appendChild(download);
    })
}