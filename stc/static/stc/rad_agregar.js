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
$("#fecha_radicacion").val(today)
$("#mes_servicio").val(mes)

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//Realizando post cada vez que el evento change ocurra en el elemento factura
$(document).ready(function() {
    $("#factura").change(function() {
        var data = { 
            "factura" : $("#factura").val(), 
            "brand" : "brand", 
            "csrfmiddlewaretoken" : getCookie('csrftoken') 
        }
        $.ajax({
            type: "POST",
            url: "/get/factura/",
            dataType: "json",
            data: data,
            success: function(data) {
                $("#convenio").val(data.convenio).parent().addClass('is-dirty');
                $("#valor_factura").val(data.valor_factura).parent().addClass('is-dirty');
                $("#empresa").val(data.empresa).parent().addClass('is-dirty');
                if (data.tipo_contrato){
                    $("#tipo_contrato").attr('checked', true).parent().addClass('is-checked');
                };
                $("#servicio").val(data.servicio).parent().addClass('is-dirty');
                $("#mes_servicio").val(data.mes_servicio).parent().addClass('is-dirty');
                alert("La factura ya existe");
            }
        });
    });
});