$(document).ready(function() {  


$("#AceptarDiag").prop("disabled", false);   

$( "#AceptarDiag" ).click(function() {        
  $("#form-diag :disabled").removeAttr('disabled');      
  $("#AceptarDiag").prop("disabled", true);    
  $( "#form-diag" ).submit(); 
  var t = setTimeout(myAjaxFunction, 2000); //wait two seconds        
  recargarDiagnosticos();
});

      

});