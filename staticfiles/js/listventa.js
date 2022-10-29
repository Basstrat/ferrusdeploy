var tblSale;



$(function () {

    tblSale = $('#data').DataTable({
        //responsive: true,
        scrollX: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: "" //si en caso una variable
        },
        columns: [
            {
                "className": 'details-control',
                "orderable": false,
                
                "defaultContent": ''
            },
            {"data": "id"},
            {"data": "cliente.nombre"},
            {"data": "fecha"},
            {"data": "total"},
            {"data": "estado"},
           
            
            
        ],
        columnDefs: [ //manejo de columnas
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return 'Q' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/venta/eliminaregistro/' + row.id + '/" class="btn btn-danger btn-sm">Eliminar</a> ';
                    buttons += '<a href="/erp/venta/editar/' + row.id + '/" class="btn btn-warning btn-sm">Editar</a> ';
                    buttons += '<a rel="details" class="btn btn-success btn-sm">Detalles</a> ';
                    buttons += '<a href="/erp/venta/imprimir/'+row.id+'/" target="_blank" class="btn btn-info btn-sm">Imprimir</a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });




$('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            console.log(data);

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                   
                    {"data": "articulo.nombre"},
                    {"data": "precio"},
                    {"data": "cant"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return 'Q' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#myModelDet').modal('show');
        })
        .on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = tblSale.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(format(row.data())).show();
                tr.addClass('shown');
            }
        });

});