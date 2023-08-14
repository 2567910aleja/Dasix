var tblVenta;
$(function () {
    tblVenta = $('#data').DataTable({
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
            {"data": "Cli.Nombres"},
            {"data": "Date_joined"},
            {"data": "Subtotal"},
            {"data": "Iva"},
            {"data": "Total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/venta/delete/' + row.id + '/" class="btn btn-danger btn-s btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    //var buttons = '<a href="/erp/venta/update/' + row.id + '/" class="btn btn-warning btn-s btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});