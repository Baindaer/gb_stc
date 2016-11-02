
function refresh(){
    window.location.href="/reportes/";
};

$(document).ready(function () {
    function exportTableToCSV() {
        $.ajax({
            url: '/reportes/exp_rad_general/',
            beforeSend: function() {
                $("#linkdesc").hide();
                $('#modal1').openModal();
            },
            success: function(result) {
                var csvData= 'data:application/csv;charset=utf-8,' + encodeURIComponent(result);
                $("#loading").hide();
                $("#dialog-content").html("El archivo se ha generado exitosamente.")
                $("#linkdesc")
                    .attr({
                        'download': "radicacion.csv",
                        'href': csvData,
                        'target': '_blank'
                    });
                $("#linkdesc").show();
            }
        });
    };
    function exportGlosaToCSV() {
        $.ajax({
            url: '/reportes/exp_gl_general/',
            beforeSend: function() {
                $("#linkdesc").hide();
                $('#modal1').openModal();
            },
            success: function(result) {
                var csvData= 'data:application/csv;charset=utf-8,' + encodeURIComponent(result);
                $("#loading").hide();
                $("#dialog-content").html("El archivo se ha generado exitosamente.")
                $("#linkdesc")
                    .attr({
                        'download': "glosas.csv",
                        'href': csvData,
                        'target': '_blank'
                    });
                $("#linkdesc").show();
            }
        });
    };
    function exportDevToCSV() {
        $.ajax({
            url: '/reportes/exp_dev_general/',
            beforeSend: function() {
                $("#linkdesc").hide();
                $('#modal1').openModal();
            },
            success: function(result) {
                var csvData= 'data:application/csv;charset=utf-8,' + encodeURIComponent(result);
                $("#loading").hide();
                $("#dialog-content").html("El archivo se ha generado exitosamente.")
                $("#linkdesc")
                    .attr({
                        'download': "devoluciones.csv",
                        'href': csvData,
                        'target': '_blank'
                    });
                $("#linkdesc").show();
            }
        });
    };
    $("#generar").on('click', function (event) {
        exportTableToCSV.apply(this);
    });
    $("#generargl").on('click', function (event) {
        exportGlosaToCSV.apply(this);
    });
    $("#generardv").on('click', function (event) {
        exportDevToCSV.apply(this);
    });
});
