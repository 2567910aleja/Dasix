var tblProductos;
var ventas={
    items:{
        Cli:'',
        Date_joined:'',
        Subtotal:0.00,
        Iva:0.00,
        Total:0.00,
        productos:[]
    },
    calcular_factura: function(){
        var Subtotal=0.00;
        var iva=$('input[name="Iva"]').val();
        $.each(this.items.productos, function(pos, dict){
            dict.Subtotal=dict.cant * parseFloat(dict.pvp);
            Subtotal+=dict.Subtotal;
        });
        this.items.Subtotal=Subtotal;
        this.items.Iva=this.items.Subtotal * iva;
        this.items.Total=this.items.Subtotal + this.items.Iva;
        $('input[name="Subtotal"]').val(this.items.Subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.Iva.toFixed(2));
        $('input[name="Total"]').val(this.items.Total.toFixed(2));
    },
    add: function(item){
        this.items.productos.push(item);
        this.list();
    },
    list: function(){
        this.calcular_factura();
        tblProductos = $('#tblProductos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.productos,
            columns: [
                { "data": "id"},
                { "data": "Nombre"},
                { "data": "cate.Nombre"},
                { "data": "pvp"},
                { "data": "cant"},
                { "data": "Subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-s btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm"  autocomplete="off" value="'+row.cant+'">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            
            // esta funcion "rowCallback" me permite modificar algunos valores de la tabla a medida que se vaya 
            // creando nuevos registros en mi tabla
            rowCallback(row, data, displayNum, displayIndex, dataIndex){
                $(row).find('input[name="cant"]').TouchSpin({
                    min:1,
                    max:100000000,
                    step:1
                });
            },
            initComplete: function(settings, json) {
    
              }
        });
    },
};

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#Date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        defaultDate: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });

    $("input[name='Iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function(){
        ventas.calcular_factura();
    }).val(0.12);

    //Busqueda de los productos

    $('input[name="search"]').autocomplete({
        source:function(request,response){
            $.ajax({
                url: window.location.pathname, 
                type: "POST",
                data: {
                    'action':'search-productos',
                    'term': request.term
                }, 
                dataType: "json",
            })
            .done(function (data) {
                response(data);
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
        // alert(`${textStatus} : ${errorThrown}`);
      })
      .always(function () {
      });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            ui.item.cant=1;
            ui.item.subtotal=0.00;
            console.log(ventas.items);
            ventas.add(ui.item);
            $(this).val('');
        }
    });

    $('.btnRemoveAll').on('click', function(){
        if(ventas.items.productos.length==0) return false;
        alert_action('Notificacion', '¿Estas seguro de eliminar todos los items de tu detalle?', function(){
            ventas.items.productos=[];
            ventas.list();
        });
    });

    // evento de cantidad
    $('#tblProductos tbody')
    .on('click', 'a[rel="remove"]', function(){
        var tr=tblProductos.cell($(this).closest('td, li')).index();
        alert_action('Notificacion', '¿Estas seguro de eliminar el producto de tu detalle?', function(){
            ventas.items.productos.splice(tr.row, 1);
            ventas.list();
        });

    })
    .on('change keyup', 'input[name="cant"]', function(){
        var cant=parseInt($(this).val());
        var tr=tblProductos.cell($(this).closest('td, li')).index();
        ventas.items.productos[tr.row].cant=cant;
        ventas.calcular_factura();
        $('td:eq(5)', tblProductos.row(tr.row).node()).html( '$'+ventas.items.productos[tr.row].Subtotal.toFixed(2));
    });

    //evento del submit
    $('form').on('submit', function (e){
        e.preventDefault();
        if (ventas.items.productos.length == 0){
            message_error('Debe tener al menos un item en su detalle de venta');
            return false;
        }
        ventas.items.Date_joined=$('input[name="Date_joined"]').val();
        ventas.items.Cli=$('select[name="Cli"]').val();
        //var parametros = $(this).serializeArray();
        var parametros = new FormData();
        parametros.append('action', $('input[name="action"]').val());
        parametros.append('ventas', JSON.stringify(ventas.items));
        submit_with_ajax(window.location.pathname,'Guardar', '¿Quiere realizar esta accion?', parametros, function (){
          location.href = '/erp/dashboard/'
        });
      });

      ventas.list();
});