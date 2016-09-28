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
};

$(document).ready(function() {
    $("#factura").change(function() {
        var data = { 
            "factura" : $("#factura").val(), 
            "csrfmiddlewaretoken" : getCookie('csrftoken') 
        }
        $.ajax({
            type: "POST",
            url: "/get/factura/",
            dataType: "json",
            data: data,
            success: function(data) {
                alert("La factura ya existe");
                $("#registrar").focus();
                $("#convenio").val(data.convenio);
                $("#valor_factura").val(data.valor_factura);
                $("#empresa").val(data.empresa);
                $('select').material_select();
                if (data.tipo_contrato){
                    $("#tipo_contrato").attr('checked', true);
                };
                $("#servicio").val(data.servicio);
                $("#mes_servicio").val(data.mes_servicio);
                Materialize.updateTextFields();
            }
        });
    });
    $("#empresa").val("GESTIONARBIENESTAR");
    $('select').material_select();
    $(window).keydown(function(event){
        if(event.keyCode == 13) {
          event.preventDefault();
          return false;
        }
    });
    $("#registrar").keydown(function(event){
        if(event.keyCode == 13) {
          $("#formulario").submit();
        }
    });
});

//Realizando post cada vez que el evento change ocurra en el elemento factura