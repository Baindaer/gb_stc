$( document ).ready(function(){   
    $(".button-collapse").sideNav();
    $(".breadcrumb:last-child").addClass("valign-wrapper");
    $('select').material_select();
    Materialize.updateTextFields();
    $("#search").keydown(function(event){
        if(event.keyCode == 13) {
          $("#consulta").submit();
        }
    });
});

function limpiarInput(id) {
    $("#id").value= "";
};