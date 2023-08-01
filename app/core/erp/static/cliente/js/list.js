$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "Nombres"},
            {"data": "Apellidos"},
            {"data": "Cedula"},
            {"data": "Cumple"},
            {"data": "Sexo"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('btnAdd').on('click', function(){
        $('input[name="name"]').val('add');
        $('#myModalCliente').modal('show');
    });

    $('form').on('submit', function (e){
        e.preventDefault();
        //var parametros = $(this).serializeArray();
        var parametros = new FormData(this);
        submit_with_ajax(window.location.pathname,'Guardar', '¿Quiere realizar esta accion?', parametros, function (){
          location.reload();
        });
      })
});
