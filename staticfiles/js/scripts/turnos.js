$(document).ready(function() {  



$.fn.datepicker.dates['es'] = {
    days: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
    daysShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"],
    months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
    today: "Hoy"
  };
  
   $('.datepicker').datepicker({
          format: "dd/mm/yyyy",
          language: "es",
          autoclose: true,
          todayHighlight: true
    });

    $('.datepicker').each(function(){
        $(this).datepicker();
    });

    
$("#id_empresa").change(function(){
    var id =  $("#id_empresa").val();
    if (id =='') {id=0;};
    $('#cargando').show();
    $.getJSON('/recargar_empleados_empresa/'+id,{},
    function (c) {
        var ide = $("#id_empleado").val();
        $("#id_empleado").empty().append('<option value="">---</option>');
        $.each(c["empleados"], function (idx, item) {
            jQuery("<option/>").text(item['nombre']).attr("value", item['id']).appendTo("#id_empleado");
        })
        $('#id_empleado').trigger("chosen:updated");  
        $('#id_empleado').val(ide).trigger('chosen:updated');
                    
    });      
    $('#cargando').hide();
}); 

$("#id_empleado").chosen({
            no_results_text: "Empleado inexistente...",
            placeholder_text_single:"Seleccione un Empleado",
        });

if ($('#id_tipo_form').val()=='ALTA'){  
  $("#id_empresa").trigger("change");
}else{
  
  $("#id_empresa").trigger("change");

  
};
   



});