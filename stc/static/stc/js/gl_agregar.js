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
$("#fecha_glosa").val(today)

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
                $("#fecha_glosa").focus();
                Materialize.updateTextFields();
                $('select').material_select();
            }
        });
    });
    $("#formulario").keydown(function(event){
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