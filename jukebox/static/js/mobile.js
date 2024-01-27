// mobile.js


var intervalPlayerTick;
var elapsed;

/* On Load */
$(function() {
    loadView("home");
    initPlayer(refreshMobileUI);
});

/* AJAX View Handler */
addEventListener("hashchange", (event) => {
    const route = window.location.hash.split('?')[0].slice(1);   
    loadView(route);
});
function loadView(route){
    console.log(route)
    $('#view-container').html('');
    $("#footer ul.nav a").removeClass('active');
    $('#footer ul.nav a[href="/#' + route + '"]').addClass('active');
    $.get('/view/mobile/'+route, function(data){
        $('#view-container').html(data);
        if (route == "search"){
            $('#search').focus()
        }
    });
}

/* Refresh Mobile UI */
function refreshMobileUI(){
    console.log('refreshMobileUI');

    seekUpdate();

    // Play/Pause Toggle
    if (JUKEBOX.status.state == 'play') {
        $('.player-btn-play').addClass('hidden');
        $('.player-btn-pause').removeClass('hidden');
    }
    else {
        $('.player-btn-play').removeClass('hidden');
        $('.player-btn-pause').addClass('hidden');
    }

    // Volume Toggle
    if (!("volume" in JUKEBOX.status)) {
        $('.player-btn-volume').hide();
        $('.player-btn-mute').hide();
        $('.player-btn-fixed').show();
    } else { 
        if (JUKEBOX.status.volume == 0) {
            $('.player-btn-volume').hide();
            $('.player-btn-mute').show();
            $('.player-btn-fixed').hide();
        } else {
            $('.player-btn-volume').show();
            $('.player-btn-mute').hide();
            $('.player-btn-fixed').hide();
        }
    }

    // Random Button (OFF / REPEAT / REPEAT ONE)
    if (Number(JUKEBOX.status.repeat) == 0 && Number(JUKEBOX.status.single) == 0) {
        $('#btn-player-repeat').removeClass('on');
        $('#btn-player-repeat').removeClass('hidden');
        $('#btn-player-repeat-1').addClass('hidden');
    } else if (Number(JUKEBOX.status.repeat) == 1 && Number(JUKEBOX.status.single) == 0) {
        $('#btn-player-repeat').addClass('on');
        $('#btn-player-repeat').removeClass('hidden');
        $('#btn-player-repeat-1').addClass('hidden');
    } else if (Number(JUKEBOX.status.repeat) == 1 && Number(JUKEBOX.status.single) == 1) {
        $('#btn-player-repeat').addClass('hidden');
        $('#btn-player-repeat-1').addClass('on');
        $('#btn-player-repeat-1').removeClass('hidden');
    }
       

    // Shuffle Button
    if (Number(JUKEBOX.status.random) == 1) {
        $('#btn-player-shuffle').addClass('on');
    } else {
        $('#btn-player-shuffle').removeClass('on');
    }
    
    // Track Info
    if (!JUKEBOX.currentsong.id) {
        // Nothing Playing
        $('#trackid').val('');
        $('.player-artist').html('&nbsp;');
        $('.player-album').html('&nbsp;');
        $('.player-title').html('&nbsp;');
        $('#img-album').attr('src', '/static/img/album.png');
    }
    else if ($('#trackid').val() != JUKEBOX.currentsong.id){
        $('#trackid').val(JUKEBOX.currentsong.id);
        $('.player-artist').html(JUKEBOX.currentsong.artist);
        $('.player-album').html(JUKEBOX.currentsong.album);
        $('.player-title').html(JUKEBOX.currentsong.title);
        $('#img-album').attr('src', '/api/cover/' + JUKEBOX.currentsong.id);
    }

    // Refresh Queue 
    if ($('#queue')[0]) {
        $.get('/view/mobile/queue', function(data){
            $('#view-container').html(data);
        });
    }

}
