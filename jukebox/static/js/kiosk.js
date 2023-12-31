$(document).keydown(function(e){
    console.log( "Handler for `keypress` called.", e.which);
    if (e.which == 39) {
        console.log('Right')
        playerNextTrack()
    } else if (e.which == 37) {
        console.log('Left');
        playerPrevTrack()
    }
});

$(function(){
    refreshKiosk();
    initPlayer(refreshKiosk);
});

function refreshKiosk(){
    if ($('#kiosk')[0]) {
        console.log('refreshKiosk')
        $.get('/view/desktop/kiosk', function(data){
          $('#kiosk').html(data);
      });
    }
}