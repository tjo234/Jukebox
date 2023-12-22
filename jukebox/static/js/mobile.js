// mobile.js

/*
-------------------------------------------------------------------------------

    AJAX View Handlers

-------------------------------------------------------------------------------
*/
$(function() {
    loadView("home");
    initPlayer();
});
addEventListener("hashchange", (event) => {
    const route = window.location.hash.split('?')[0].slice(1);   
    loadView(route);
});
function loadView(route){
    console.log(route)
    $('#view-container').html('');
    $("#footer ul.nav a").removeClass('active');
    $('#footer ul.nav a[href="/#' + route + '"]').addClass('active');
    $.get('/view/'+route, function(data){
        $('#view-container').html(data);
    });
}