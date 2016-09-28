var dialog = document.querySelector('dialog');

function refresh(){
    window.location.href="/reportes/";
};

$(document).ready(function () {
    function exportTableToCSV() {
        $.ajax({
            url: '/reportes/exp_rad_general/',
            beforeSend: function() {
                $("#linkdesc").hide();
                dialog.showModal();
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
    $("#generar").on('click', function (event) {
        exportTableToCSV.apply(this);
    });
});
