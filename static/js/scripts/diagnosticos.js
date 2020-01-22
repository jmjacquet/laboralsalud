$(document).ready(function() {  


$("#AceptarDiag").prop("disabled", false);   

$( "#AceptarDiag" ).click(function() {        
  $("#form-diag :disabled").removeAttr('disabled');      
  $("#AceptarDiag").prop("disabled", true);    
  $( "#form-diag" ).submit(); 
 recargarDiagnosticos(); //wait two seconds        
 
});

      

});