$(document).ready(function() {  


$("#AceptarPat").prop("disabled", false);   

$( "#AceptarPat" ).click(function() {        
  $("#form-pat :disabled").removeAttr('disabled');      
  $("#AceptarPat").prop("disabled", true);    
  $( "#form-pat" ).submit();         
  recargarPatologias();
});

      

});