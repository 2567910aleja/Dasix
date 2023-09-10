$(function(){
    $("#data").DataTable({
      responsive: true,
      autoWidth: false,
      destroy: true,
      deferRender: true,
      ajax: {
        url: window.location.pathnam,
        type: "POST",
        data: { action: "searchdata" }, // parametros
        dataSrc: "",
      },
      columns: [
        { data: "id" },
        { data: "first_name" },
        { data: "last_name" },
        { data: "username" },
        { data: "Date_joined" },
        { data: "image" },
        { data: "groups" },
        { data: "id" },
      ],
      columnDefs: [
        {
          targets: [-3],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            return (
              '<img src="' + row.image + '" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">'
            );
          },
        },
        {
          targets: [-2],
          class: 'text-center',
          orderable: false,
          render: function (data, type, row) {
              var html = '';
              $.each(row.groups, function (key, value) {
                  html += '<span class="badge badge-success">' + value.name + '</span> ';
              });
              return html;
          }
      },

        {
          targets: [-1],
          class: "text-center",
          orderable: false,
          render: function (data, type, row) {
            var buttons =
              '<a  href="/user/update/' +
              row.id +
              '/" class="btn btn-primary btn-s btn-flat btn-bg-morado-2"><i class="fas fa-edit"></i></a> ';
            buttons +=
              '<a href="/user/delete/' +
              row.id +
              '/" type="button" class="btn btn-danger btn-s btn-flat"><i class="fas fa-trash-alt"></i></a>';
            return buttons;
          },
        },
      ],
      initComplete: function (settings, json) {},
    });
})