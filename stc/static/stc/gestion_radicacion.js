document.getElementById("id_registro").value= 0;
document.getElementById("factura").value= " ";
function getRow(x) {
    var index_registro = document.getElementById("dash").rows[x.rowIndex].cells[0].innerHTML;
    document.getElementById("id_registro").value = index_registro;
    document.getElementById("factura").value = index_registro;
};