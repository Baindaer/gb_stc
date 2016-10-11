var date = new Date();
var day = date.getDate();
var month = date.getMonth() + 1;
var year = date.getFullYear();
if (month < 10) 
  month = "0" + month;
if (day < 10) 
  day = "0" + day;
var today = year + "-" + month + "-" + day;   
var mes = year + "-" + month;
$("#fecha_actualizacion").val(today)

function getRow(x) {
    var index_registro = document.getElementById("dash").rows[x.rowIndex].cells[0].innerHTML;
    var index_registro_factura = document.getElementById("dash").rows[x.rowIndex].cells[1].innerHTML;
    var index_registro_estado = document.getElementById("dash").rows[x.rowIndex].cells[7].innerHTML;
    $("#id_registro").val(index_registro);
    $("#factura").val(index_registro_factura);
    $("#estado").val(index_registro_estado);
    $('select').material_select();
    Materialize.updateTextFields();
};