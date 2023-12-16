/*
	kiosk.js
*/

$(function(){
	refreshKiosk();
	waitForChange();
});
function waitForChange(){
	$.getJSON('/player/idle', function(data){
        console.log('Change received: ' + data)
        refreshKiosk()
        waitForChange();
    });
}
function refreshKiosk(){
	$.get('/view/kiosk', function(data){
        $('#kiosk').html(data);
    });
}