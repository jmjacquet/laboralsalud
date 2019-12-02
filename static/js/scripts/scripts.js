    alertify.defaults.transition = "slide";
    alertify.defaults.theme.ok = "btn btn-xs btn-primary";
    alertify.defaults.theme.cancel = "btn btn-xs btn-danger";
    alertify.defaults.theme.input = "form-control";        

    $('[data-toggle=tooltip]').tooltip();     
    

    toastr.options = {
      "closeButton": true,
      "debug": false,
      "positionClass": "toast-top-center",
      "onclick": null,
      "showDuration": "1000",
      "hideDuration": "1000",
      "timeOut": "5000",
      "extendedTimeOut": "1000",
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut",          
    };

      $("input[type=number]").click(function(){
            this.select()
          });   
   
    
	 if(!alertify.errorAlert){
      alertify.dialog('errorAlert',function factory(){
    return{
            build:function(){
                var errorHeader = '<span class="fa fa-times-circle fa-2x" '
                +    'style="vertical-align:middle;margin-right:10px;color:#e10000;text-align:left;">'
                + '</span> ¡ATENCIÓN!';
                this.setHeader(errorHeader);
            }
        };
    },true,'alert'); 
    };

    if(!alertify.successAlert){
      alertify.dialog('successAlert',function factory(){
    return{
            build:function(){
                var successHeader = '<span class="fa fa-check-circle fa-2x" '
                +    'style="vertical-align:middle;margin-right:10px;color:#6aca5f;text-align:left;">'
                + '</span> ¡ATENCIÓN!';
                this.setHeader(successHeader);
            }
        };
    },true,'alert'); 
    };

    if(!alertify.warningAlert){
      alertify.dialog('warningAlert',function factory(){
    return{
            build:function(){
                var warningHeader = '<span class="fa fa-check-circle fa-2x" '
                +    'style="vertical-align:middle;color:#FFFF00;margin-right:10px;text-align:left;">'
                + '</span> ¡ATENCIÓN!';
                this.setHeader(warningHeader);
            }
        };
    },true,'alert'); 


 function recargarEmpleados(){
        $.getJSON('/recargar_empleados/',{},
        function (c) {
            $("#id_empleado").empty().append('<option value="">---</option>');
            $.each(c["empleados"], function (idx, item) {
                jQuery("<option/>").text(item['nombre']).attr("value", item['id']).appendTo("#id_empleado");
            })
            $('#id_empleado').trigger("chosen:updated");            
        });      
    };

function recargarDiagnosticos(){
        $.getJSON('/recargar_diagnosticos/',{},
        function (c) {
            $("#id_aus_diagn").empty().append('<option value="">---</option>');
            $.each(c["diagnosticos"], function (idx, item) {
                jQuery("<option/>").text(item['nombre']).attr("value", item['id']).appendTo("#id_aus_diagn");
            })
            $('#id_aus_diagn').trigger("chosen:updated");            
        });      
    };
    
function recargarPatologias(){
        $.getJSON('/recargar_patologias/',{},
        function (c) {
            $("#id_aus_grupop").empty().append('<option value="">---</option>');
            $.each(c["patologias"], function (idx, item) {
                jQuery("<option/>").text(item['nombre']).attr("value", item['id']).appendTo("#id_aus_grupop");
            })
            $('#id_aus_grupop').trigger("chosen:updated");            
        });      
    };


function recargarMedicos(){
        $.getJSON('/recargar_medicos/',{},
        function (c) {
            $("#id_aus_medico").empty().append('<option value="">---</option>');
            $.each(c["medicos"], function (idx, item) {
                jQuery("<option/>").text(item['nombre']).attr("value", item['id']).appendTo("#id_aus_medico");
            })
            $('#id_aus_medico').trigger("chosen:updated");
            $("#id_art_medico").empty().append('<option value="">---</option>');
            $.each(c["medicos"], function (idx, item) {
                jQuery("<option/>").text(item['nombre']).attr("value", item['id']).appendTo("#id_art_medico");
            })
            $('#id_art_medico').trigger("chosen:updated");
           
        });      
    };
   


    

};  