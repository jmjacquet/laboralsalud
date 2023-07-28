$(document).ready(function() {



$.fn.datepicker.dates['es'] = {
    days: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
    daysShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"],
    months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
    today: "Hoy"
  };
   $('#id_empleado_form-fecha_nac').datepicker({
          format: "dd/mm/yyyy",
          language: "es",
          autoclose: true,
          todayHighlight: true,
          daysOfWeekDisabled : [0,6],
    });

   $('#id_fecha').datepicker({
          format: "dd/mm/yyyy",
          language: "es",
          autoclose: true,
          todayHighlight: true,
          daysOfWeekDisabled : [0,6],
    });


const userAgent = navigator.userAgent.toLowerCase();
const isTablet = /(ipad|tablet|(android(?!.*mobile))|(windows(?!.*phone)(.*touch))|kindle|playbook|silk|(puffin(?!.*(IP|AP|WP))))/.test(userAgent);

if (isTablet==false) {

$("#id_turno_empleado").chosen({
        no_results_text: "Empleado inexistente...",
        placeholder_text_single:"Seleccione un Empleado",
        allow_single_deselect: true,
    });

  $("#id_turno_empresa").chosen({
      no_results_text: "Empresa inexistente...",
      placeholder_text_single:"Seleccione una Empresa",
      allow_single_deselect: true,
  });
};

$('#id_hora').timepicker({
   className: "form-control",
   timeFormat:'H:i',
   minTime : '08:00',
   maxTime : '21:00',
   forceRoundTime: true,
   useSelect: true,
});

$("#id_turno_empresa").change(function(){
    var id =  $("#id_turno_empresa").val();
    if (id =='') {id=0;};
    $('#cargando').show();
    $.getJSON('/recargar_empleados_empresa/'+id,{},
    function (c) {
        var ide = $("#id_turno_empleado").val();
        $("#id_turno_empleado").empty().append('<option value="">---</option>');
        $.each(c["empleados"], function (idx, item) {
            jQuery("<option/>").text(item['nombre']).attr("value", item['id']).appendTo("#id_turno_empleado");
        })
        if (isTablet==false) {
        $('#id_turno_empleado').trigger("chosen:updated");
        $('#id_turno_empleado').val(ide).trigger('chosen:updated');
      };

    });
    $('#cargando').hide();
});

$( "#Buscar" ).click(function() {
      var e = $.Event( "keyup", { which: 13 } );
      $('#id_empresa_form-cuit').trigger(e);
 });
$("#id_empresa_form-cuit").keyup(function(e){
  if(e.which === 13) {
     consulta = $("#id_empresa_form-cuit").val();
     if (consulta.length<6)
     {
      alertify.alert('Búsqueda por CUIT','Debe ingresar un CUIT válido!.');
      $("#id_empresa_form-cuit").focus();
     }
     else{
        $.ajax({
        data: {'cuit': consulta},
        url: '/buscarDatosAPICUIT/',
        type: 'get',
        cache: true,
        beforeSend: function(){
            $('#cargando').show();
        },
        complete: function(){
            $('#cargando').hide();
        },
        success : function(data) {
             if (data!='')
                {
                    if (data['tipoPersona']=='JURIDICA'){
                      $("#id_empresa_form-razon_social").val(data['razonSocial']);
                    }else{
                      $("#id_empresa_form-razon_social").val(data['apellido']+' '+data['nombre']);
                    };
                }else
                {
                  $("#id_empresa_form-cuit").val('');
                  $("#id_empresa_form-razon_social").val('');
                  $("#id_empresa_form-cuit").focus();
                  alertify.alert('Búsqueda por CUIT','No se encontraron contribuyentes con el CUIT '+consulta+'. <br>El servicio de consulta de CUIT ONline (AFIP) puede estar momentáneamente interrumpido. Vuelva a intentarlo mas tarde.');
                }
        },
        error : function(message) {
             $('#cargando').hide();
             alertify.alert('Búsqueda por CUIT','No se encontraron contribuyentes. <br>El servicio de consulta de CUIT ONline (AFIP) puede estar momentáneamente interrumpido. Vuelva a intentarlo mas tarde.');
             console.log(message);
          }
      });
      }
    }
  });

if ($('#id_tipo_form').val()=='EDICION'){
  $("#id_empleado").trigger("change");
} else {
    $("#id_turno_empresa").trigger("change");
};


$( "#Aceptar" ).click(function() {        
       $("#form-alta :disabled").removeAttr('disabled');      
        $("#Aceptar").prop("disabled", true);    
        $( "#form-alta" ).submit();         
      });


});