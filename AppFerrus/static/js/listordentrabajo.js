var tbldetalle;



$(function () {

    tbldetalle = $('#data').DataTable({
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
            {"data": "definicion"},
           
            
            
        ],
        columnDefs: [ //manejo de columnas
            {
                
            },
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/orden_trabajo/eliminar/' + row.id + '/" class="btn btn-danger btn-sm">Eliminar</a> ';
                    buttons += '<a rel="details" class="btn btn-success btn-sm">Detalles</a> ';
                    buttons += '<a href="/erp/orden_trabajo/imprimir/'+row.id+'/" target="_blank" class="btn btn-info btn-sm">Imprimir</a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });




$('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tbldetalle.cell($(this).closest('td, li')).index();
            var data = tbldetalle.row(tr.row).data();
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
                
                    {"data": "cant"},
                 
                ],
                columnDefs: [
                    {
                       
                    },
                    {
                       
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#myModelDet').modal('show');
        })
        .on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = tbldetalle.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(format(row.data())).show();
                tr.addClass('shown');
            }
        });

});