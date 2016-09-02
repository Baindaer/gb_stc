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
document.getElementById("consultar").style.visibility = "hidden";
document.getElementById("mes_reporte").value = mes;

function realizarConsulta(){
    var form = document.getElementById("consultar");
    form.submit();
};
function getRow(x) {
    var index_registro = document.getElementById("dash").rows[x.rowIndex].cells[0].innerHTML;
    document.getElementById("factura").value = index_registro;
    realizarConsulta();
};