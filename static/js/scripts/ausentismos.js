$(document).ready(function() {  

const userAgent = navigator.userAgent.toLowerCase();
const isTablet = /(ipad|tablet|(android(?!.*mobile))|(windows(?!.*phone)(.*touch))|kindle|playbook|silk|(puffin(?!.*(IP|AP|WP))))/.test(userAgent);

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

$("input[type=number]").click(function(){
            this.select()
          });



if (isTablet==false) {
$("#id_aus_grupop").chosen({
      no_results_text: "Patología inexistente...",
      placeholder_text_single:"Seleccione una Patología",
      allow_single_deselect: true,
  });

$("#id_aus_diagn").chosen({
      no_results_text: "Diagnóstico inexistente...",
      placeholder_text_single:"Seleccione un Diagnóstico",
      allow_single_deselect: true,
  });

$("#id_aus_medico").chosen({
      no_results_text: "Médico inexistente...",
      placeholder_text_single:"Seleccione un Médico",
      allow_single_deselect: true,
  });

$("#id_art_medico").chosen({
      no_results_text: "Médico inexistente...",
      placeholder_text_single:"Seleccione un Médico",
      allow_single_deselect: true,
  });

};

$("#id_empleado").change(function(){
  var id =  $("#id_empleado").val();
  if (id!='')
    {
          $.ajax({
                data: {'id': id},
                url: '/buscarDatosEntidad/',
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
                          $("#apellido_y_nombre").text(data['apellido_y_nombre']); 
                          $("#nro_doc").text(data['nro_doc']); 
                          if (data['fecha_nac']==null){
                            $("#fecha_nac").text(''); }
                            else{
                          $("#fecha_nac").text(moment(data['fecha_nac']).format("DD/MM/YYYY")); 
                          }
                          $("#legajo").text(data['legajo']); 
                          $("#edad").text(data['edad']+' años'); 
                          $("#telcel").text((data['telefono']||'')+' / '+(data['celular']||'')); 
                          $("#email").text(data['email']); 
                          $("#cod_postal").text(data['cod_postal']);
                          $("#domicilio").text(data['domicilio']);
                          $("#provincia").text(data['provincia']);
                          $("#localidad").text(data['localidad']);
                          $("#art").text(data['art']); 
                          
                          $("#empresa").text(data['empresa']); 
                          if (data['empr_fingreso']==null){
                            $("#empr_fingreso").text(''); 
                          }else{
                            $("#empr_fingreso").text(moment(data['empr_fingreso']).format("DD/MM/YYYY")); };
                          $("#trab_cargo").text(data['trab_cargo']); 
                          if (data['trab_fingreso']==null){
                            $("#trab_fingreso").text(''); 
                          }else{
                          $("#trab_fingreso").text(moment(data['trab_fingreso']).format("DD/MM/YYYY")); };
                          if (data['trab_fbaja']==null){
                            $("#trab_fbaja").text(''); 
                          }else{
                          $("#trab_fbaja").text(moment(data['trab_fbaja']).format("DD/MM/YYYY"));}; 
                          $("#trab_armas").text(data['trab_armas']); 
                          $("#trab_tareas_dif").text(data['trab_tareas_dif']); 
                          $("#trab_preocupac").text(data['trab_preocupac']); 
                          if (data['trab_preocup_fecha']==null){
                            $("#trab_preocup_fecha").text(''); 
                          }else{
                          $("#trab_preocup_fecha").text(moment(data['trab_preocup_fecha']).format("DD/MM/YYYY")); };
                          $("#antig_empresa").text(data['antig_empresa']+' años'); 
                          $("#antig_trabajo").text(data['antig_trabajo']+' años'); 
                          
                        }
                        else{                 
                          $("#apellido_y_nombre").text(''); 
                          $("#nro_doc").text(''); 
                          $("#fecha_nac").text('');
                          $("#legajo").text('');
                          $("#edad").text('');
                          $("#telcel").text('');
                          $("#email").text('');
                          $("#art").text('');
                          $("#cod_postal").text('');
                          $("#domicilio").text('');
                          $("#provincia").text('');
                          $("#localidad").text('');
                          $("#empresa").text(''); 
                          $("#empr_fingreso").text(''); 
                          $("#trab_cargo").text('');
                          $("#trab_fingreso").text('');
                          $("#trab_fbaja").text('');
                          $("#trab_preocupac").text('');
                          $("#trab_armas").text('');
                          $("#trab_tareas_dif").text('');
                          $("#trab_preocup_fecha").text('');
                          $("#antig_empresa").text('');
                          $("#antig_trabajo").text('');
                        };

                        
                },
                error : function(message) {
                     /*alertify.alert('Búsqueda por CUIT','No se encontró el Proveedor.');*/
                     console.log(message);
                  }
              });
     
    }else{                 
            $("#apellido_y_nombre").text(''); 
            $("#nro_doc").text(''); 
            $("#fecha_nac").text('');
            $("#legajo").text('');
            $("#edad").text('');
            $("#telcel").text('');
            $("#email").text('');
            $("#cod_postal").text('');
            $("#domicilio").text('');
            $("#provincia").text('');
            $("#localidad").text('');
            $("#art").text('');
            $("#empresa").text(''); 
            $("#empr_fingreso").text(''); 
            $("#trab_cargo").text('');
            $("#trab_fingreso").text('');
            $("#trab_fbaja").text('');
            $("#trab_armas").text('');
            $("#trab_tareas_dif").text('');
            $("#trab_preocup_fecha").text('');
            $("#antig_empresa").text('');
            $("#antig_trabajo").text('');
            $("#trab_preocupac").text('');
          };

}); 


$('#id_tipo_ausentismo').change(function()
{
  var tipos = ['1','4','5','6', '7','8']
    var id =  $("#id_tipo_ausentismo").val();
  if (tipos.indexOf(id) !== -1){
    $('#tab_ausencia').show();
    $('#tab_art').hide();
    $('#titulo').html('DATOS DE LA AUSENCIA')
  }else{
    $('#tab_art').show();
    $('#tab_ausencia').hide();
    $('#titulo').html('DATOS DE LA ART')
  }
  
})


$('#id_aus_fcrondesde').change(function()
{  
  if ($("#id_aus_fcronhasta").val()=='')
  {
    $("#id_aus_fcronhasta").val($('#id_aus_fcrondesde').val());
  };
  diasRestantes($('#id_aus_fcrondesde'),$("#id_aus_fcronhasta"),$("#id_aus_diascaidos"));
});

$('#id_aus_fcronhasta').change(function()
{  
  if ($("#id_aus_fcrondesde").val() == '')
  {
    $("#id_aus_fcrondesde").val($('#id_aus_fcronhasta').val());
  };
  diasRestantes($('#id_aus_fcrondesde'),$("#id_aus_fcronhasta"),$("#id_aus_diascaidos"));
});



 function diasRestantes(desde,hasta,dias){
        var a = moment(desde.val(),'D/M/YYYY');
        var b = moment(hasta.val(),'D/M/YYYY');
        var diffDays = b.diff(a, 'days')+1;        
        if (diffDays < 0) {diffDays=0};
        dias.val(diffDays);
    };

$('#cargando').hide();
if ($('#id_tipo_form').val()=='EDICION'){  
  $("#id_empleado").trigger("change");
} else {
  

  $("#id_empresa").change(function(){
      var id =  $("#id_empresa").val();
      if (id =='') {id=0;};
      $('#cargando').show();
      
       $.ajax({
                dataType: 'json',
                url: '/recargar_empleados_empresa/'+id,
                async: false,
                type: 'get',
                cache: true,          
                beforeSend: function(){
                $('#cargando').show();
                },
                complete: function(){
                    $('#cargando').hide();
                },
                success : function(data) {
                  $("#id_empleado").empty().append('<option value="">---</option>');
                  $.each(data["empleados"], function (idx, item) {
                      jQuery("<option/>").text(item['nombre']).attr("value", item['id']).appendTo("#id_empleado");
                  })
                  if (isTablet==false) {
                    $('#id_empleado').trigger("chosen:updated");  
                   };
                    $("#id_empleado").trigger("change");      
                 
                },
                error : function(message) {
                  console.log(message);
                   $('#cargando').hide();
                }
        });
        $('#cargando').hide();
     
      $('#cargando').hide();
  }); 


    if (isTablet==false) {
    $("#id_empleado").chosen({
        no_results_text: "Empleado inexistente...",
        placeholder_text_single:"Seleccione un Empleado",
        allow_single_deselect: true,
    });
    };
    if ($("#id_empleado").val()==''){
    $("#id_empresa").trigger("change");
  }else{
    $("#id_empleado").trigger("change");  
  }
};
if (isTablet==false) {
  $("#id_empleado").chosen({
          no_results_text: "Empleado inexistente...",
          placeholder_text_single:"Seleccione un Empleado",
          allow_single_deselect: true,
      });
 };
$("#id_tipo_ausentismo").trigger("change");



$( "#Guardar" ).click(function() {        
   $("#form-ausentismos :disabled").removeAttr('disabled');      
    $("#Guardar").prop("disabled", true);    
    $( "#form-ausentismos" ).submit();         
  });






 });