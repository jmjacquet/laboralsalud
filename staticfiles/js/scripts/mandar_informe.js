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
  
$("#enviando").hide();
 $("input[type=number]").click(function(){
            this.select()
          });


  $( "#AceptarSeleccion" ).click(function() {
    datos = [];
    id = $("#id_ausentismo_id").val()

    if ((id == '')||(id=='undefined')) {
      formData = $('#form-informe').serialize()+'&'+$("#btnInforme").val();    
    }else{
      formData = $('#form-informe').serialize();
    };

    console.log(formData);
    
     
    $("#enviando").show();        
    if ((id == '')||(id=='undefined')) {
      $.ajax({      
      url :"/ausentismos/generar_informe/",
      data : formData,
      type: "POST",            
      dataType : "json",
       success: function(data) {                   
           $("#enviando").hide();
          if (data['cant']<=0){
                  alertify.errorAlert(data["message"]);     
                }
                else{                       
                 alertify.successAlert(data['message'],function(){ location.reload(); });             
                   };
          },
          error: function(data) {            
              console.log(data);
              $("#enviando").hide();
            }
        });
      }else{
        $.ajax({      
        url :"/ausentismos/generar_informe_individual/"+id+"/",
        data : formData,
        type: "POST",            
        dataType : "json",
         success: function(data) {                   
             $("#enviando").hide();
            if (data['cant']<=0){
                    alertify.errorAlert(data["message"]);     
                  }
                  else{                       
                   alertify.successAlert(data['message'],function(){ location.reload(); });             
                     };
            },
            error: function(data) {            
                console.log(data);
                $("#enviando").hide();
              }
          });
      }
   
   
});


});