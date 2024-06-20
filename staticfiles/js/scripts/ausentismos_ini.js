
$(document).ready(function() {

moment.locale('es');


 $('.datepicker').datepicker({
        format: "dd/mm/yyyy",
        language: "es",
        autoclose: true,
        todayHighlight: true
  });

  $('.datepicker').each(function(){
      $(this).datepicker();
  });

const userAgent = navigator.userAgent.toLowerCase();
const isTablet = /(ipad|tablet|(android(?!.*mobile))|(windows(?!.*phone)(.*touch))|kindle|playbook|silk|(puffin(?!.*(IP|AP|WP))))/.test(userAgent);

if (isTablet==false) {
  $("#id_empresa").chosen({
      no_results_text: "Empresa inexistente...",
      placeholder_text_single:"Seleccione una Empresa",
      allow_single_deselect: true,
      width:"100%",
  });
  };

$("#checkall").click (function () {
     var checkedStatus = this.checked;
    $("input[class='tildado']").each(function () {
        $(this).prop("checked", checkedStatus);
        $(this).change();
     });
  });

var listado = [];

var tabla = $('#ausentismos').DataTable({
            "language": {
                "decimal": ",",
                "thousands": ".",
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "No hay registros en esta tabla",
                "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix": "",
                "sSearch": "Buscar:",
                "sUrl": "",
                "sInfoThousands": ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst": "Primero",
                    "sLast": "Ãšltimo",
                    "sNext": "Siguiente",
                    "sPrevious": "Anterior"
                },
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                },
                "decimal": ",",
                "thousands": ".",
            },

         "columnDefs": [ {
                  "targets"  : 'no-sort',
                  "orderable": false,
                }],
           "paging":   true,
           "lengthMenu": [[25, 50, -1], [25, 50, "Todos"]],
           "autoWidth": false,
           "order": [],
           "colReorder": false,
           "searching": true,
            fixedHeader: {
              header: false,
              footer: false
              },
            responsive: false,
            dom: "Bf<'row'<'col-sm-12'tr>>"+"<'row'<'col-sm-3'l><'col-sm-9'ip>>",
            buttons: [
                {
                    extend:    'colvis',
                    text:      '<i class="fa fa-list"></i>',
                    titleAttr: 'Ver/Ocultar',
                    className: 'btnToolbar',
                },
                {
                    extend:    'copyHtml5',
                    text:      '<i class="fa fa-files-o"></i>',
                    titleAttr: 'Copiar',
                    exportOptions: { columns: ':visible' },
                    className: 'btnToolbar',
                },
                {
                    extend:    'excel',
                    text:      '<i class="fa fa-file-excel-o"></i>',
                    titleAttr: 'Excel',
                    filename: 'AUSENTISMOS',
                    exportOptions: {  modifier: {
                                        page: 'current'
                                    },
                                      columns: '.imprimir',
                                      format: {
                                      body: function(data, row, column, node) {
                                        var floatVal = function (i) {
                                            if (typeof i === "number") {
                                                return i;
                                            } else if (typeof i === "string") {
                                                i = i.replace(/\$/g, "");
                    i = i.replace(/\,/g ,"");
                    i = i.replace(/\./g, "");
                                                var result = parseFloat(i)/100;
                                                // console.log(result);
                                                if (isNaN(result)) {
                                                    try {
                                                        var result = $jq(i).text();
                                                        result = parseFloat(result);
                                                        if (isNaN(result)) { result = 0 };
                                                        return result * 1;
                                                    } catch (error) {
                                                        return 0;
                                                    }
                                                } else {
                                                    return result * 1;
                                                }
                                            } else {
                                                alert("Unhandled type for totals [" + (typeof i) + "]");
                                                return 0
                                            }
                                        };
                                          data = $('<p>' + data + '</p>').text();
                                          return (node.className=='importe') ? floatVal(data)  : data;
                                      }
                                    }},
                    className: 'btnToolbar',
                },

                {
                    extend:    'pdfHtml5',
                    text:      '<i class="fa fa-file-pdf-o"></i>',
                    titleAttr: 'PDF',footer: true,
                    exportOptions: { columns: '.imprimir'},
                    orientation: 'landscape',
                    className: 'btnToolbar',
                },
                {
                    extend: 'print',
                    text:      '<i class="fa fa-print"></i>',
                    titleAttr: 'Imprimir',
                    exportOptions: { columns: '.imprimir' },
                    className: 'btnToolbar',
                },
            ],
            PreDrawCallback:function(){
            $("#cargando").show();
            },
            initComplete: function () {
               // this.api().columns().every( function () {[0, 1, 9]
                $("#ausentismos").show();
                  this.fnAdjustColumnSizing();
                $("#cargando").hide();
            },

        });

$("input[class='tildado']" ,tabla.rows().nodes()).change(function() {
        str1 = '/ausentismos/generar_informe/?';
        str2 = '';
        checkbox=this;
        id = checkbox.value;
        if (checkbox.checked) {
                //Agrego al array de aus seleccionados
                listado.push(id);
                $(checkbox).closest('tr').toggleClass('selected', checkbox.checked);
        } else {
            if ($(checkbox).closest('tr').hasClass('selected')) {
                $(checkbox).closest('tr').removeClass('selected');
            };
            var listado2=[];
            //Regenero el array de ids selecionados sin el que acabo de quitar
            for( var i = 0; i < listado.length; i++){
                if ( listado[i] != id) listado2.push(listado[i]);
                };
            listado=listado2;
        };
        //Armo el String para los botones
        for (var i = 0; i < listado.length; i++) {
                if (str2 == '') {
                    str2 = str2 + 'id=' + listado[i];
                } else {
                    str2 = str2 + '&id=' + listado[i];
                };
        };
      $('#btnInforme').val(str2)
      $('#btnEliminar').val(str2);

    });

 $('#btnEliminar').click(function() {
        if (listado.length == 0) {
            alertify.errorAlert("¡Debe seleccionar algún Ausentismo!");
        } else {
            alerta = alertify.dialog('confirm').set({
                'labels': {
                    ok: 'Aceptar',
                    cancel: 'Cancelar'
                },
                'message': '¿Desea Eliminar los Ausentismos seleccionados?',
                transition: 'fade',
                'onok': function() {
                    $.ajax({
                        url: "/ausentismos/ausentismo_eliminar_masivo?" + $('#btnEliminar').val(),
                        type: "get",
                        dataType: 'json',
                        success: function(data) {
                            window.location.href = window.location.href
                        }
                    });
                },
                'oncancel': function() {
                    return true;
                }
            });
            alerta.setting('modal', true);
            alerta.setHeader('ELIMINAR AUSENTISMOS');
            alerta.show();
            return true;
        }
    });

$("#enviando").hide();
$('#btnInforme').click(function(){
     if (listado.length == 0) {
            alertify.errorAlert("¡Debe seleccionar algún Ausentismo!");
        } else {
           return abrir_modal('/ausentismos/generar_informe/?'+$('#btnInforme').val());
        }

});

$('#btnImprimirInforme').click(function(){
     if (listado.length == 0) {
            alertify.errorAlert("¡Debe seleccionar algún Ausentismo!");
        } else {
           return abrir_modal('/ausentismos/imprimir_informe/?'+$('#btnInforme').val());
        }

})


})
