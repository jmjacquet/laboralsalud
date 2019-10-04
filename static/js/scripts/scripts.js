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
    };