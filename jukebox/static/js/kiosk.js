$(function(){
    initPlayer(onPlayerChanged);
});

function onPlayerChanged(change){
    console.log('onPlayerChanged', change, JUKEBOX);

    if ($('#kiosk')[0]) {
        $.get('/view/desktop/fullscreen', function(data){
          $('#kiosk').html(data);
      });
    }
}