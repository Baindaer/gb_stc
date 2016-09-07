var dialog = document.querySelector('dialog');

function mostrarDetalle(x) {
    var index_registro = document.getElementById("dash_devoluciones").rows[x.rowIndex].cells[1].innerHTML;
    var index_oculto_detalle = document.getElementById("datos_ocultos").rows[x.rowIndex-1].cells[0].innerHTML;
    var index_oculto_gestion = document.getElementById("datos_ocultos").rows[x.rowIndex-1].cells[1].innerHTML;
    document.getElementById("dialog-content").innerHTML = "<b><h5>DETALLE: </h5></b>" + index_oculto_detalle + "<br><b><h5>GESTION: </h5></b>" + index_oculto_gestion;
    dialog.showModal();
  }
