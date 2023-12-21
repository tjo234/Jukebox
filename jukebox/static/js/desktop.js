// desktop.js

$(function(){
	refreshKiosk();
	initPlayer();
});

function refreshKiosk(){
	$.get('/view/kiosk', function(data){
        $('#kiosk').html(data);
    });
}