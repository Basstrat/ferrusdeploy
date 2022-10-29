var tblarticulos;
var cotizacion1 = {
    items:  {
    idorden_compra_material: 0.00,
    nombre: '',
    articulo: 0.00,
    observaciones: '',
    cantidadcompra: 0.00,
    subtotal: 0.00,
    total: 0.00,
    material: [],
    subtotal: 0.00,
    },
    
    calcularcotizacion1: function() {
        var subtotal = 0.00;
        
        $.each(this.items.material, function (pos, dict) {//para recorrer articulo{
            console.log(pos);
            console.log(dict);
            dict.totalcompra = -Number(dict.totalcompra);
            dict.totalcompra = Number(dict.cantidadcompra) - Number(dict.stock);
            dict.subtotal = dict.totalcompra * dict.precio_unidad;
            subtotal+=dict.subtotal //aqui sumo mi columna
            
        });
        this.items.subtotal = subtotal; //aqui digo que la suma de articulos se igual a subtotal
        $('input[name="subtotal"]').val(this.items.subtotal);
        
      
        this.items.total = this.items.subtotal;
        $('input[name="total"]').val(this.items.total.toFixed(2));


    },
       



    list: function () {
        this.calcularcotizacion1();
        tblarticulos= $('#tblarticulo').DataTable( { //aqui asigno mi variable table
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.material,
            columns: [
                {"data": "idmaterial" },
                {"data": "nombre"},
                {"data": "cant"},
                {"data": "stock"},
                {"data": "cantidadcompra"},
                {"data": "totalcompra"},
                {"data": "precio_unidad"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    return '<a rel="remove" class="btn btn-danger btn-sm">Eliminar</a>';
            }, 
        },
    
            {
                targets: [6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    return 'Q'+parseFloat(data).toFixed();
        },
    },
    
    {
        targets: [3],
        class: 'text-center',
        orderable: false,
        render: function (data, type, row){
            return '<input type="text" name="stock" class="form-control form-control-sm" autocomplete="off" value="'+row.stock+'"> ';
    },
    },
    {
        targets: [4],
        class: 'text-center',
        orderable: false,
        render: function (data, type, row){
            return parseFloat(data).toFixed();
    },
    },
    {
        
    },
    {
        targets: [5],
        class: 'text-center',
        orderable: false,
        render: function (data, type, row){
            return '<input type="text" name="totalcompra" class="form-control form-control-sm" autocomplete="off" value="'+row.totalcompra+'"> ';
    },
    },
    
    ],

    //a medida que se vaya creado un nuevo registro se pueden ir modificando cierto datos
    rowCallback(row, data, displayNum, displayIndex, dataIndex){ 
        //row contien mis campos, y data la informacion
        $(row).find('input[name="stock"]').TouchSpin({
            min: 0,
            max: 100,
            step: 1
        })
        .val(0);

        $(row).find('input[name="totalcompra"]').TouchSpin({
            min: 0,
            max: 100,
            step: 1
        })
        .val(0);

       
    },
    initComplete: function(settings, json){
    
    }
        });
    
    },};

    

    




$(function() {
    $('.select2').select2( {
        theme: "bootstrap4",
        language: 'es'
    });

    $('#fecha').datetimepicker({ /*este es el formato de mi fecha*/ 
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
    
    
        
});




//busqueda de productos
$('input[name="buscar"]').autocomplete({ //nombre de mi barra de busqueda
    source: function (request, response) {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_articulo', //llamar esta en mi vista action POST
                'variablebusqueda': request.term
            },
            dataType: 'json',
        }).done(function (data) {
            response(data);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            //alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    },
    delay: 500,
    minLength: 1,
    select: function (event, ui) {
        event.preventDefault();
        //item es la variable que viene del form
        //ui.item.cantidad = cant;
        ui.item.subtotal = 0.00;
        cotizacion1.items.material.push(ui.item); //para agregar mi items a mi estrucutra de variable cotizacion1
        console.log(cotizacion1.items);
        cotizacion1.list();//para que se enlisten los items
        $(this).val('');

    }
});


$('.btnRemoveAll').on('click', function(){
    cotizacion1.items.material = [];
    cotizacion1.list();
});


//evento cantidad articulos  //al cambio y que se actulizce
$('#tblarticulo tbody')
.on('click','[rel=remove]', function(){ //cuando haga click en el boton eliminar
    var tr = tblarticulos.cell($(this).closest('td, li')).index(); //llamo a mi tabla
    cotizacion1.items.material.splice(tr.row, 1); //esta es mi posicion actual
    cotizacion1.list();
})
.on('change', 'input[name="stock"]', function() {
    var stock = parseFloat($(this).val()); //para guardar el dato que cambio a enteri
    var tr = tblarticulos.cell($(this).closest('td, li')).index();
    console.log(tr);
    var data = tblarticulos.row(tr.row).node(); //ubicacion de mis cambios
    console.log(data);
    cotizacion1.items.material[tr.row].stock = stock; //aguardo la cantidad que cambie
    cotizacion1.calcularcotizacion1();
    $('td:eq(4)',tblarticulos.row(tr.row).node()).html(cotizacion1.items.material[tr.row].cantidadcompra = $('input[name="cantidadcompra"]').val() * cotizacion1.items.material[tr.row].cant);
    $('td:eq(5)',tblarticulos.row(tr.row).node()).html(cotizacion1.items.material[tr.row].totalcompra = cotizacion1.items.material[tr.row].cantidadcompra - cotizacion1.items.material[tr.row].stock );
    $('td:eq(7)',tblarticulos.row(tr.row).node()).html('Q'+cotizacion1.items.material[tr.row].subtotal.toFixed(2));

});
//cuando guarde mi post
$('form').on('submit', function (e){
    e.preventDefault();  
    var parameters = new FormData(this);
    parameters.append('action', $('input[name="action"]').val()); //aqui mando los parametros dek html con append
    parameters.append('products', JSON.stringify(cotizacion1.items.material)); //para convertir json a string
    submit_with_ajax(window.location.pathname, 'Notificacion', 'Desea guardar?', parameters, function (){
        location.href =  '/erp/orden_compra/listado/';
    })


})
});




