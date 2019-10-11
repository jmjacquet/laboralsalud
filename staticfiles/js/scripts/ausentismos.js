$(document).ready(function() {  


$("input[type=number]").click(function(){
            this.select()
          });

  // $.fm({        
  //         custom_callbacks: {
  //             "recargarC": function(data, options) {
  //                recargarClientes();
  //                },
  //             "recargarV": function(data, options) {
  //                recargarVendedores();
  //                }
  //             }
  //   });

  $("#id_empleado").chosen({
            no_results_text: "Empleado inexistente...",
            placeholder_text_single:"Seleccione un Empleado",
            allow_single_deselect: true,
        });

$("#id_empleado").change(function(){
  var id =  $("#id_empleado").val();
  if (id!='')
    {
          $.ajax({
                data: {'id': id},
                url: '/buscarDatosEntidad/',
                type: 'get',
                cache: true,          
                beforeSend: function(){
                $('#cargando').show();
                },
                complete: function(){
                    $('#cargando').hide();
                },
                success : function(data) {
                     
                     if (data!='')
                        {
                          $("#apellido_y_nombre").text(data['apellido_y_nombre']); 
                          $("#nro_doc").text(data['nro_doc']); 
                          $("#fecha_nac").text(moment(data['fecha_nac']).format("DD/MM/YYYY")); 
                          $("#legajo").text(data['legajo']); 
                          $("#edad").text(data['edad']+' años'); 
                          $("#telcel").text(data['telefono']+'/'+data['celular']); 
                          $("#email").text(data['email']); 
                          $("#art").text(data['art']); 

                          $("#empresa").text(data['empresa']); 
                          $("#empr_fingreso").text(moment(data['empr_fingreso']).format("DD/MM/YYYY")); 
                          $("#trab_cargo").text(data['trab_cargo']); 
                          $("#trab_fingreso").text(moment(data['trab_fingreso']).format("DD/MM/YYYY")); 
                          $("#trab_fbaja").text(moment(data['trab_fbaja']).format("DD/MM/YYYY")); 
                          $("#trab_armas").text(data['trab_armas']); 
                          $("#trab_tareas_dif").text(data['trab_tareas_dif']); 
                          $("#trab_preocupac").text(data['trab_preocupac']); 
                          $("#trab_preocup_fecha").text(moment(data['trab_preocup_fecha']).format("DD/MM/YYYY")); 
                          $("#antig_empresa").text(data['antig_empresa']+' años'); 
                          $("#antig_trabajo").text(data['antig_trabajo']+' años'); 
                          
                        }
                        else{                 
                          $("#apellido_y_nombre").text(''); 
                          $("#nro_doc").text(''); 
                          $("#fecha_nac").text('');
                          $("#legajo").text('');
                          $("#edad").text('');
                          $("#telcel").text('');
                          $("#email").text('');
                          $("#art").text('');

                          $("#empresa").text(''); 
                          $("#empr_fingreso").text(''); 
                          $("#trab_cargo").text('');
                          $("#trab_fingreso").text('');
                          $("#trab_fbaja").text('');
                          $("#trab_preocupac").text('');
                          $("#trab_armas").text('');
                          $("#trab_tareas_dif").text('');
                          $("#trab_preocup_fecha").text('');
                          $("#antig_empresa").text('');
                          $("#antig_trabajo").text('');
                        };

                        
                },
                error : function(message) {
                     /*alertify.alert('Búsqueda por CUIT','No se encontró el Proveedor.');*/
                     console.log(message);
                  }
              });
     
    }else{                 
            $("#apellido_y_nombre").text(''); 
            $("#nro_doc").text(''); 
            $("#fecha_nac").text('');
            $("#legajo").text('');
            $("#edad").text('');
            $("#telcel").text('');
            $("#email").text('');
            $("#art").text('');
            $("#empresa").text(''); 
            $("#empr_fingreso").text(''); 
            $("#trab_cargo").text('');
            $("#trab_fingreso").text('');
            $("#trab_fbaja").text('');
            $("#trab_armas").text('');
            $("#trab_tareas_dif").text('');
            $("#trab_preocup_fecha").text('');
            $("#antig_empresa").text('');
            $("#antig_trabajo").text('');
            $("#trab_preocupac").text('');
          };

  }); 




$('#cargando').hide();
$("#id_empleado").trigger("change");


 });