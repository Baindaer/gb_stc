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
$("#fecha_respuesta").val(today)

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

$(document).ready(function() {
    $("#formulario").keydown(function(event){
        if(event.keyCode == 13) {
          event.preventDefault();
          return false;
        }
    });
    $("#respuesta_reg").keydown(function(event){
        if(event.keyCode == 13) {
          $("#formulario").submit();
        }
    });
    $("#glosa").change(function() {
        var glosa = $('#glosa').val();
        var data = { 
            "glosa" : glosa, 
            "csrfmiddlewaretoken" : getCookie('csrftoken'),
        };
        $.ajax({
            type: "POST",
            url: "/get/glosa/",
            dataType: "json",
            data: data,
            success: function(data) {
                $("#factura").val(data.factura);
                $("#valor_glosa").val(data.valor_glosa);
                $("#extemporaneidad").val(data.extemporaneidad);
            }
        });
    });
    Materialize.updateTextFields();
    $('select').material_select();
});

function getRow(x) {
    var index_registro = document.getElementById("dash").rows[x.rowIndex].cells[0].innerHTML;
    $("#num_glosa").val(index_registro);
    $('#modal1').openModal();
    Materialize.updateTextFields();
};

function post(path, params, method) {
    method = method || "post";  // Asignar como tipo post si no se especifica
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

function imprimir() {
    var respuesta = $('#respuesta').val();
    var cookie = getCookie('csrftoken');
    post('/glosas/respuestas/imprimir', {respuesta: respuesta, csrfmiddlewaretoken: cookie });
}

function eliminar() {
    var respuesta = $('#respuesta').val();
    var cookie = getCookie('csrftoken');
    post('/glosas/respuestas/agregar', {respuesta: respuesta, btn_submit: 'respuesta_elim', csrfmiddlewaretoken: cookie });
}