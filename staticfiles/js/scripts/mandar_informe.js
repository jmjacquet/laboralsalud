$(document).ready(function() { 
$("#enviando").hide();
 $("input[type=number]").click(function(){
            this.select()
          });


  $( "#AceptarSeleccion" ).click(function() {
    datos = [];
    formData = $('#form-informe').serialize()+'&'+$("#btnInforme").val();
    $("#enviando").show();
    $.ajax({
      url : "/ausentismos/generar_informe/" ,
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
});


});