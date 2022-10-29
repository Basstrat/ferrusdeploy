var tblarticulos;
var cotizacion1 = {
    items:  {
    nombre: '',
    descripcion: '',
    articulo: '',
    mano_de_obra: 0.00,
    otrosgastos: 0.00,
    subtotal: 0.00,
    precio: 0.00,
    porciento: 0.00,
    material: [],
    subtotal: 0.00,
    },
    
    calcularcotizacion1: function() { // estaes?si
    
    var porciento = $('input[name="porciento"]').val();
    var subtotal = 0.00;
    const mano_de_obra = $('input[name="mano_de_obra"]').val();
    const otrosgastos = $('input[name="otrosgastos"]').val();
    
        $.each(this.items.material, function (pos, dict) {//para recorrer articulo{
            console.log(pos);
            console.log(dict);
            dict.subtotal = dict.cant * dict.precio_unidad;
            subtotal+=dict.subtotal //aqui sumo mi columna
         
        });

        this.items.subtotal = subtotal ; //aqui digo que la suma de articulos se igual a subtotal
        $('input[name="subtotal"]').val(this.items.subtotal);
    
        this.items.porciento = this.items.subtotal * porciento;
        $('input[name="porcientocal"]').val(this.items.porciento.toFixed(2)); 

        this.items.totalgastos = Number(mano_de_obra) + Number(otrosgastos);
        $('input[name="totalotrosgastos"]').val(this.items.totalgastos);
        


        this.items.precio = this.items.subtotal +  this.items.porciento + this.items.totalgastos;
        $('input[name="precio"]').val(this.items.precio);


       


    },
    
    list: function () {
        this.calcularcotizacion1();
        tblarticulos= $('#tblarticulo').DataTable( { //aqui asigno mi variable table
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.material,
            columns: [
                {"data": "id" },
                {"data": "nombre"},
                {"data": "descripcion"},
                {"data": "precio_unidad"},
                {"data": "cant"},
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
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    return 'Q'+parseFloat(data).toFixed();
        },
    },
    
    {
        targets: [-2],
        class: 'text-center',
        orderable: false,
        render: function (data, type, row){
            return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off"> ';
    },
    },
    {
        targets: [-1],
        class: 'text-center',
        orderable: false,
        render: function (data, type, row){
            return 'Q'+parseFloat(data).toFixed();
    },
    },
    
    ],

    //a medida que se vaya creado un nuevo registro se pueden ir modificando cierto datos
    rowCallback(row, data, displayNum, displayIndex, dataIndex){ 
        //row contien mis campos, y data la informacion
        $(row).find('input[name="cant"]').TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        })
        .val(1);
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


$("input[name='porciento']").TouchSpin({
    min: 0,
    max: 100,
    step: 0.01,
    decimals: 2,
    boostat: 5,
    maxboostedstep: 10,
    postfix: '%'
}).on('change', function () { //cuando yo haga un cambio
    cotizacion1.calcularcotizacion1();
})
    .val(0.12);

    $("input[name='mano_de_obra']").TouchSpin({
        min: 0,
        max: 100000,
        step: 10.00,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: 'Q'
    }).on('change', function () { //cuando yo haga un cambio
        cotizacion1.calcularcotizacion1();
    })
        .val(0.0);


        $("input[name='otrosgastos']").TouchSpin({
            min: 0,
            max: 100000,
            step: 10.00,
            decimals: 2,
            boostat: 5,
            maxboostedstep: 10,
            postfix: 'Q'
        }).on('change', function () { //cuando yo haga un cambio
            cotizacion1.calcularcotizacion1();
        })
            .val(0.0);

//busqueda de productos
$('input[name="buscar"]').autocomplete({ //nombre de mi barra de busqueda
    source: function (request, response) {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_material', //llamar esta en mi vista action POST
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
        ui.item.cantidad = 1.00;
        ui.item.subtotal = 0.00;
        cotizacion1.items.material.push(ui.item); //para agregar mi items a mi estrucutra de variable cotizacion1
        console.log(cotizacion1.items);
        cotizacion1.list();//para que se enlisten los items
        $(this).val('');

    }
});




//evento cantidad articulos  //al cambio y que se actulizce
$('#tblarticulo tbody')
.on('click','[rel=remove]', function(){ //cuando haga click en el boton eliminar
    var tr = tblarticulos.cell($(this).closest('td, li')).index(); //llamo a mi tabla
    cotizacion1.items.material.splice(tr.row, 1); //esta es mi posicion actual
    cotizacion1.list();
})
.on('change', 'input[name="cant"]', function() {
    var cant = parseFloat($(this).val()); //para guardar el dato que cambio a enteri
    var tr = tblarticulos.cell($(this).closest('td, li')).index();
    console.log(tr);
    var data = tblarticulos.row(tr.row).node(); //ubicacion de mis cambios
    console.log(data);
    cotizacion1.items.material[tr.row].cant = cant; //aguardo la cantidad que cambie
    cotizacion1.calcularcotizacion1();
    $('td:eq(5)',tblarticulos.row(tr.row).node()).html('Q'+cotizacion1.items.material[tr.row].subtotal.toFixed(2));

});

//cuando guarde mi post
$('form').on('submit', function (e){
    e.preventDefault();
    cotizacion1.items.mano_de_obra = $('input[name="mano_de_obra"]').val();
    cotizacion1.items.otrosgastos = $('input[name="otrosgastos"]').val();
    cotizacion1.items.fecha = $('input[name="fecha"]').val(); //aqui llamo a los valores de mis inputs html
    cotizacion1.items.nombre = $('input[name="nombre"]').val();
    cotizacion1.items.descripcion = $('input[name="descripcion"]').val();
    cotizacion1.items.precio = $('input[name="precio"]').val();
    var parameters = new FormData();

    parameters.append('action', $('input[name="action"]').val()); //aqui mando los parametros dek html con append
    parameters.append('cotizacion1', JSON.stringify(cotizacion1.items)); //para convertir json a string
    
    for (const pair of parameters.entries()) {
        console.log(`${pair[0]}, ${pair[1]}`);
    }
    
    submit_with_ajax(window.location.pathname, 'Notificacion', 'Desea guardar?', parameters, function (){
        location.href =  '/erp/articulo/listado/';
    })


})
});




