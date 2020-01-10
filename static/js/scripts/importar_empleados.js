$(document).ready(function() {  
   $('#cargando').hide();
   $( "#Procesar" ).click(function() {        
        $('#cargando').show();
        $("#Procesar").prop("disabled", true);    
        $( "#importador" ).submit();         
      });
 });