var verts={
    items:{
        Cli:'',
        Date_joined:'',
        Subtotal:0.00,
        Iva:0.00,
        Total:0.00,
        productos:[]
    },
    add: function(){

    }
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
                    'action':'search-productos',cd Dasix
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
            console.log(ui.item)
        },
    });
});