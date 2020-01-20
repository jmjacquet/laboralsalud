$(document).ready(function() { 
$("#enviando").hide();
 $("input[type=number]").click(function(){
            this.select()
          });


  $( "#AceptarSeleccion" ).click(function() {
    datos = [];
    var accion = $( "#id_accion" ) .val()        
    if (accion == '1'){
        $("#enviando").show();
        formData = $('#form-informe').serialize()+'&'+$("#btnInforme").val();
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
    } else {      
      url="/ausentismos/imprimir_informe/?"+$("#btnInforme").val();
      var win = window.open(url, '_blank');
      location.reload();
      win.focus();      
    };
        
});


});