var tblCliente;
var modal_title;
function getData(){
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
                        var buttons = '<a href="#" rel="edit" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
    
            }
        });
    })
}
    
    $(function(){
        modal_title = $('.modal-title');
        getData();
        $('.btnAdd').on('click', function () {
            $('input[name="action"]').val('add');
            modal_title.find('span').html('Creación de un cliente');
            console.log(modal_title.find('i'));
            modal_title.find('i').removeClass().addClass('fas fa-plus');
            $('form')[0].reset();
            $('#myModalCliente').modal('show');
        });
        
        $('#data tbody').on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html('Edición de un cliente');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblCliente.cell($(this).closest('td, li')).index();
            var data = tblCliente.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="Nombres"]').val(data.Nombres);
            $('input[name="Apellidos"]').val(data.Apellidos);
            $('input[name="Cedula"]').val(data.Cedula);
            $('input[name="Cumple"]').val(data.Cumple);
            $('input[name="Direccion"]').val(data.Direccion);
            $('select[name="Sexo"]').val(data.Sexo.id);
            $('#myModalCliente').modal('show');
        });
    
        $('#myModalCliente').on('shown.bs.modal', function () {
            //$('form')[0].reset();
        });

    $('form').on('submit', function (e){
        e.preventDefault();
        //var parametros = $(this).serializeArray();
        var parametros = new FormData(this);
        submit_with_ajax(window.location.pathname,'Guardar', '¿Quiere realizar esta accion?', parametros, function (){
            $('#myModalCliente').modal('hide');
            tblCliente.ajax.reload();
        });
      });
    });
