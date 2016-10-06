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
$("#fecha_respuesta").val(today);

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
    $('#glosa').val("");
    $("#glosa").change(function() {
        var glosa = $('#glosa').val();
        var separador = glosa.indexOf("@")+1;
        var glosa_id = glosa.substring(separador,separador+5);
        var data = { 
            "glosa_id" : glosa_id, 
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
    $("#respuesta").change(function() {
        var respuesta = $('#respuesta').val();
        var data = { 
            "respuesta" : respuesta, 
            "csrfmiddlewaretoken" : getCookie('csrftoken'),
        };
        $.ajax({
            type: "POST",
            url: "/get/respuesta/",
            dataType: "json",
            data: data,
            success: function(data) {
                $("#convenio").val(data.convenio).attr("disabled", true);
                $("#empresa").val(data.empresa).attr("disabled", true);
                $("#fecha_respuesta").val(data.fecha_respuesta).attr('readonly', true);
                $("#referencia").val(data.referencia).attr('readonly', true).parent().addClass('is-dirty');
                if (data.cerrado){
                    $("#cargar").html("Cerrado")
                } else {
                    $("#cargar").html("Cargar")
                }
            },
            error: function() {
                $("#convenio").attr("disabled", false);
                $("#empresa").attr("disabled", false);
                $("#fecha_respuesta").attr('readonly', false);
                $("#referencia").attr('readonly', false)
            }
        });
    });
    $("#main-action").click(function() {
        var glosa = $('#glosa').val();
        var separador = glosa.indexOf("@")+1;
        var glosa_id = glosa.substring(separador,separador+5);
        if (parseInt($('#aceptado_ips').val()) > parseInt($("#valor_glosa").val())){
            alert("El valor aceptado "+$('#aceptado_ips').val()+"  no puede ser mayor al valor de la glosa " + $("#valor_glosa").val())
        } else {
            var data = { 
                "submit" : 'agregar', 
                "glosa_id":glosa_id,
                "respuesta": $('#respuesta').val(),
                "convenio": $('#convenio').val(),
                "empresa": $('#empresa').val(),
                "referencia": $('#referencia').val(),
                "fecha_respuesta": $('#fecha_respuesta').val(),
                "aceptado_ips": $('#aceptado_ips').val(),
                "gestion": $('#gestion').val(),
                "csrfmiddlewaretoken" : getCookie('csrftoken'),
            };
            $.ajax({
                type: "POST",
                url: "/glosas/respuesta/agregar",
                dataType: "json",
                data: data,
                success: function(data) {
                    var a = '<td class="mdl-data-table__cell--non-numeric">';
                    var an = '<td>';
                    var c = '</td>';
                    var factura = $('#factura').val();
                    var valor_glosa = $('#valor_glosa').val();
                    var extemporaneidad = $('#extemporaneidad').val();
                    var aceptado_ips = $('#aceptado_ips').val();
                    var gestion = $('#gestion').val();
                    alert(data.mensaje);
                    $('#dash').append('<tr>' + 
                        a + data.glosa_id + c + 
                        a + factura + c + 
                        an + valor_glosa + c + 
                        a + extemporaneidad + c + 
                        an + aceptado_ips + c + 
                        a + gestion + c +
                        '</tr>'
                    );
                    var pre_glosa = $('#glosa').val();
                    $("#glosa").find('[value="'+pre_glosa+'"]').remove();
                    $('#glosa').val("");
                    $('#factura').val("");
                    $('#valor_glosa').val("");
                    $('#extemporaneidad').val("");
                    $('#aceptado_ips').val("");
                    $('#gestion').val("");
                }
            });
        }
    });
});