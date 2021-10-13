$(document).ready(function() {

  $("#id_agrupamiento").change(function(){
      var id =  $("#id_agrupamiento").val();
      if (id =='') {id=0;};
      $('#cargando').show();

       $.ajax({
                dataType: 'json',
                url: '/recargar_empresas_agrupamiento/' + id,
                async: false,
                type: 'get',
                cache: true,
                beforeSend: function(){
                $('#cargando').show();
                },
                complete: function(){
                    $('#cargando').hide();
                },
                success : function(data) {
                  $("#id_empresa").empty().append('<option value="">---</option>');
                  $.each(data, function (idx, item) {
                      jQuery("<option/>").text(item['nombre']).attr("value", item['id']).appendTo("#id_empresa");
                  })
                    $('#id_empresa').trigger("chosen:updated");
                    $("#id_empresa").trigger("change");

                },
                error : function(message) {
                  console.log(message);
                   $('#cargando').hide();
                }
        });
        $('#cargando').hide();

      $('#cargando').hide();
  });

  if ($("#id_empresa") == undefined) {
    $("#id_agrupamiento").change();
  }else{
    var id =  $("#id_empresa").val();
    $("#id_agrupamiento").change();
    $("[name='empresa']").val(id).trigger("chosen:updated");
  }

});