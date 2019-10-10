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
  // var id =  $("#id_entidad").val();
  // if (id!='')
  //   {
  //         $.ajax({
  //               data: {'id': id},
  //               url: '/comprobantes/buscarDatosEntidad/',
  //               type: 'get',
  //               cache: true,          
  //               success : function(data) {
                     
  //                    if (data!='')
  //                       {
  //                         $("#id_cliente_categ_fiscal").val(data['fact_categFiscal']); 
  //                         if (data['dcto_general']==''){
  //                           $("#id_cliente_descuento").val(data['dcto_general'])
  //                         }else {$("#id_cliente_descuento").val(0);};                          
  //                         if (data['lista_precios']!=''){
  //                            $("#id_lista_precios").find('option[value="'+data['lista_precios']+'"]').attr("selected",true);
  //                         };

  //                         var tot = data['saldo_sobrepaso'];
  //                         if (tot>0){
  //                           alertify.alert("TOPE SALDO PERMITIDO CLIENTES","¡El saldo pendiente sobrepasa al tope permitido por <b>$"+tot+"</b>!"); 
  //                         };
  //                       }
  //                       else{                 
  //                        $("#id_cliente_categ_fiscal").val(5); 
  //                         $("#id_cliente_descuento").val(0); 
  //                       };

  //                       calcularTotales();
  //               },
  //               error : function(message) {
  //                    /*alertify.alert('Búsqueda por CUIT','No se encontró el Proveedor.');*/
  //                    console.log(message);
  //                 }
  //             });

  //     if ($('#id_tipo_form').val()=='ALTA')
  //     {        
  //           $.ajax({
  //                 data: {'id': id},
  //                 url: '/comprobantes/setearLetraCPB/',
  //                 type: 'get',
  //                 cache: true,          
  //                 success : function(data) {
                       
  //                      if (data!='')
  //                         {
  //                           $("#id_letra").val(data[0]); 
  //                           $("#id_letra").trigger("change");
  //                         }
                         
  //                 },
  //                 error : function(message) {
  //                      /*alertify.alert('Búsqueda por CUIT','No se encontró el Proveedor.');*/
  //                      console.log(message);
  //                   }
  //               });
  //       }
  //   }

  }); 




 });