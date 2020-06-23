$(document).ready(function() {  


$("input[type=number]").click(function(){
            this.select()
          });

  $("#id_empresa").chosen({
      no_results_text: "Empresa inexistente...",
      placeholder_text_single:"Seleccione una Empresa",
      allow_single_deselect: true,
  });
  
  
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

$('#id_empr_fingreso').change(function()
{    
  antiguedad($('#id_empr_fingreso'),'',$("#id_empr_antig"));
});

$('#id_trab_fingreso').change(function()
{    
  if ($('#id_trab_fbaja').val()!=''){
    antiguedad($('#id_trab_fingreso'),$('#id_trab_fbaja'),$("#id_trab_antig"));
  }else{
  antiguedad($('#id_trab_fingreso'),'',$("#id_trab_antig"));};
});

function antiguedad(fecha,fbaja,anios){        
        var desde = moment(fecha.val(),'DD/MM/YYYY');
        if (fbaja==''){
          var hasta = new Date()
        }else{
          var hasta = moment(fbaja.val(),'DD/MM/YYYY');
        };        
        var diffDays = Math.floor(moment(hasta).diff(moment(desde,"DD/MM/YYYY"),'years',true))
        if (diffDays < 0) {diffDays=0};
        anios.val(diffDays);
    };

$('#id_trab_fbaja').change(function(){
  $("#id_trab_fingreso").trigger("change");
  });

if ($("#id_empr_fingreso").val()!=''){
  $("#id_empr_fingreso").trigger("change");
};
if ($("#id_trab_fingreso").val()!=''){
$("#id_trab_fingreso").trigger("change");};




   $( "#Aceptar" ).click(function() {        
       $("#form-empl :disabled").removeAttr('disabled');      
        $("#Aceptar").prop("disabled", true);    
        $( "#form-empl" ).submit();                 
        recargarEmpleadosEmpresa($("#id_empresa").val());
      });

});    