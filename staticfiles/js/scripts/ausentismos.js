$(document).ready(function() {  

$.fn.datepicker.dates['es'] = {
    days: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
    daysShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"],
    months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
    today: "Hoy"
  };
  
 $('.dateinput').datepicker({
        format: "dd/mm/yyyy",
        language: "es",
        autoclose: true,
        todayHighlight: true
  });

  $('.dateinput').each(function(){
      $(this).datepicker();
  });

$("input[type=number]").click(function(){
            this.select()
          });

  $.fm({        
          custom_callbacks: {
              "recargarE": function(data, options) {
                 recargarEmpleados();
                 },
              "recargarM": function(data, options) {
                 recargarMedicos();
                 },
              "recargarGP": function(data, options) {
                 recargarPatologias();
                 },
              "recargarD": function(data, options) {
                 recargarDiagnosticos();
                 },
              }
    });

$("#id_empleado").chosen({
      no_results_text: "Empleado inexistente...",
      placeholder_text_single:"Seleccione un Empleado",
      allow_single_deselect: true,
  });

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
                          $("#fecha_nac").text(moment(data['fecha_nac']).format("DD/MM/YYYY")); 
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
  var id =  $("#id_tipo_ausentismo").val();
  if (id==1){
    $('#tab_ausencia').show();
    $('#tab_art').hide();
  }else{
    $('#tab_art').show();
    $('#tab_ausencia').hide();
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


$('#id_art_fcrondesde').change(function()
{  
  if ($("#id_art_fcronhasta").val()=='')
  {
    $("#id_art_fcronhasta").val($('#id_art_fcrondesde').val());
  };
  diasRestantes($('#id_art_fcrondesde'),$("#id_art_fcronhasta"),$("#id_art_diascaidos"));
});

$('#id_art_fcronhasta').change(function()
{  
  if ($("#id_art_fcrondesde").val() == '')
  {
    $("#id_art_fcrondesde").val($('#id_art_fcronhasta').val());
  };
  diasRestantes($('#id_art_fcrondesde'),$("#id_art_fcronhasta"),$("#id_art_diascaidos"));
});



 function diasRestantes(desde,hasta,dias){
        var a = moment(desde.val(),'D/M/YYYY');
        var b = moment(hasta.val(),'D/M/YYYY');
        var diffDays = b.diff(a, 'days');        
        if (diffDays < 0) {diffDays=0};
        dias.val(diffDays);
    };

$('#cargando').hide();
$("#id_empleado").trigger("change");
$("#id_tipo_ausentismo").trigger("change");


 });