var ventas={
    items:{
        Cli:'',
        Date_joined:'',
        Subtotal:0.00,
        Iva:0.00,
        Total:0.00,
        productos:[]
    },
    add: function(item){
        this.items.productos.push(item);
        this.list();
    },
    list: function(){
        $('#tblProductos').DataTable({
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
                { "data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-s btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3, -1],
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
                        return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off" value="'+row.cant+'">';
                    }
                },
            ],
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
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });

    $("input[name='Iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });

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
});