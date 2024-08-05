$(document).ready(function() {
    $('.bntsuscribir').click(function(event) {
        // Evitar que se envíe el formulario por defecto
        event.preventDefault();
        var usera = $(this).data('usuario');
        window.location.href = "/pago/"+usera+"/";
        
        // Realizar la solicitud AJAX a la vista de Django
        /*$.ajax({
            type: 'GET',
            url: '/agg_sub/'+ usera +'/',  
            success: function(data) {
                // Recargar la página después de que se complete la solicitud AJAX
                window.location.reload();
            }
        });*/
    });
});
