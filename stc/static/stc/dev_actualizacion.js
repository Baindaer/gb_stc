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
document.getElementById("fecha_gestion").value = today;
document.getElementById("id_registro").value= 0;
document.getElementById("factura").value= " ";
function getRow(x) {
    var index_registro = document.getElementById("dash").rows[x.rowIndex].cells[0].innerHTML;
    var index_registro_factura = document.getElementById("dash").rows[x.rowIndex].cells[1].innerHTML;
    var index_estado = document.getElementById("dash").rows[x.rowIndex].cells[6].innerHTML;
    document.getElementById("id_registro").value = index_registro;
    document.getElementById("factura").value = index_registro_factura;
    document.getElementById("estado").value = index_estado;
};