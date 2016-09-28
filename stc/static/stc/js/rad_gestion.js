function getRow(x) {
    var index_registro = document.getElementById("dash").rows[x.rowIndex].cells[0].innerHTML;
    var index_registro_factura = document.getElementById("dash").rows[x.rowIndex].cells[1].innerHTML;
    $("#factura").val(index_registro)
    Materialize.updateTextFields();
};