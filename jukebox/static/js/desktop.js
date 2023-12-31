/*
-------------------------------------------------------------------------------

    Desktop App

-------------------------------------------------------------------------------
*/
const DEFAULT_ROUTE = 'home';

$(function() {
    loadView();
    initPlayer(onPlayerChanged);
});

addEventListener("hashchange", (event) => {  
    loadView();
});

function loadView(){
    const route = window.location.hash ? window.location.hash.split('?')[0].slice(1) : DEFAULT_ROUTE;
    console.log(route)

    // Update Navigation
    $("#sidebar a").removeClass('active');
    $('#sidebar a[href="/#' + route + '"]').addClass('active');

    // Hide all
    $('#views > div').hide();

    // Check for static route
    if ($('#view-' + route)[0]){
        $('#view-' + route).fadeIn();
    } else {
        // Load dynamic route
        $.get('/view/desktop/'+route, function(data){
            $('#view-container').html(data).fadeIn();
        });
    }
}

function onPlayerChanged(){
    console.log('onPlayerChanged');
}
