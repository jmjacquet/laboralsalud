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
   
    
	   