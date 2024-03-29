/*
-------------------------------------------------------------------------------

    Desktop App

-------------------------------------------------------------------------------
*/
$(function() {
    loadView();
    initPlayer(onPlayerChanged);
});

// Handle Route Changes
addEventListener("hashchange", (event) => {  
    loadView();
});

function loadView(){
    var DEFAULT_ROUTE = 'home'
    if ($('body').hasClass('mobile')) {
        DEFAULT_ROUTE = 'mobile';
    }
    const route = window.location.hash ? window.location.hash.split('?')[0].slice(1) : DEFAULT_ROUTE;
    const qs = window.location.hash ? window.location.hash.split('?')[1] : '';
    console.log('loadView', route)

    // Update Navigation
    $("#sidebar a").removeClass('active');
    $('#sidebar a[href="/#' + route + '"]').addClass('active');

    // Hide all
    $('#views > div').hide();

    $.get('/view/'+ route + '?' + qs, function(data){
        $('#view-container').html(data).fadeIn();
    });
}

function onPlayerChanged(change){
    console.log('onPlayerChanged', change, JUKEBOX);

    if('updating_db' in JUKEBOX.status){
        var s = `Database update in progress [Job: ${JUKEBOX.status.updating_db}]`;
        $('#loading').attr('title', s).show();
    } else {
        $('#loading').hide();
    }  

    // Play/Pause Toggle
    if (JUKEBOX.status.state == 'play') {
        $('.player-btn-play').addClass('hidden');
        $('.player-btn-pause').removeClass('hidden');
    }
    else {
        $('.player-btn-play').removeClass('hidden');
        $('.player-btn-pause').addClass('hidden');
    }

    // Random Button (OFF / REPEAT / REPEAT ONE)
    if (Number(JUKEBOX.status.repeat) == 0 && Number(JUKEBOX.status.single) == 0) {
        $('.player-btn-repeat').removeClass('on');
        $('.player-btn-repeat').removeClass('hidden');
        $('.player-btn-repeat-1').addClass('hidden');
    } else if (Number(JUKEBOX.status.repeat) == 1 && Number(JUKEBOX.status.single) == 0) {
        $('.player-btn-repeat').addClass('on');
        $('.player-btn-repeat').removeClass('hidden');
        $('.player-btn-repeat-1').addClass('hidden');
    } else if (Number(JUKEBOX.status.repeat) == 1 && Number(JUKEBOX.status.single) == 1) {
        $('.player-btn-repeat').addClass('hidden');
        $('.player-btn-repeat-1').addClass('on');
        $('.player-btn-repeat-1').removeClass('hidden');
    }     

    // Shuffle Button
    if (Number(JUKEBOX.status.random) == 1) {
        $('.player-btn-shuffle').addClass('on');
    } else {
        $('.player-btn-shuffle').removeClass('on');
    }

    // Track Info
    if (!('title' in JUKEBOX.currentsong)) {
        // Nothing Playing
        $('.player-artist').html('&nbsp;');
        $('.player-title').html('&nbsp;');
        $('.player-album').html('&nbsp;');
        $('.img-album').attr('src', '/static/img/album.png');
    }
    else {
        $('.player-artist').html(JUKEBOX.currentsong.artist);
        $('.player-title').html(JUKEBOX.currentsong.title);
        $('.player-album').html(JUKEBOX.currentsong.album);
        $('.img-album').attr('src', '/api/cover/'+JUKEBOX.status.songid);
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

    // Update Seek Bar
    updateSeekBarUI();

    // Refresh Queue 
    if ($('#playlist-queue')[0]) {
        $.get('/view/queue', function(data){
            $('#playlist-queue').html(data);
        });
    }

    if ($('#queue-simple')[0]) {
        $.get('/view/queue-simple', function(data){
            $('#queue-simple').html(data);
        });
    }

    if ($('#status')[0]) {
        $.get('/view/status', function(data){
            $('#status').html(data);
        });
    }

}
function getAlbumURL(album) {
    return "/static/img/albums/" + encodeURIComponent(album).replace(/%20/g,'+') + ".jpg";
}

/* UI Helpers */
function secondsToElapsed(s){
    var str_elapsed;
    if (s >= 60*60) {
        str_elapsed = new Date(s * 1000).toISOString().slice(11, 19);    
    } {
        str_elapsed = new Date(s * 1000).toISOString().slice(14, 19);    
    }
    return str_elapsed;
}

/* Seek Bar UI Refresh */
var intervalPlayerTick;
function updateSeekBarUI(){
    clearInterval(intervalPlayerTick);
    if (JUKEBOX.status.state == 'play') {
        $('.player-duration').html(JUKEBOX.status.str_duration);
        $('.player-elapsed').html(JUKEBOX.status.str_elapsed);
        $('.player-seek').attr('min', 0);
        $('.player-seek').attr('max', JUKEBOX.status.duration);
        $('.player-seek').val(JUKEBOX.status.elapsed);
        elapsed = Number.parseInt(JUKEBOX.status.elapsed);
        intervalPlayerTick = setInterval(function(){
            console.log('tick')
            elapsed++;
            $('.player-seek').val(elapsed);
            $('.player-elapsed').html(secondsToElapsed(elapsed));
        }, 1000);
    } else if (JUKEBOX.status.state == 'stop') {
        $('.player-duration').html("0:00");
        $('.player-elapsed').html("0:00");
        $('.player-seek').attr('min', 0);
        $('.player-seek').attr('max', 100);
        $('.player-seek').val(0);
        elapsed = 0;
    }
}


function changeServer(){
    const JUKEBOX_ADDR = "JUKEBOX_ADDR";
    var addr = prompt('Enter a new server location (192.168.1.100 or jukebox.local)');
    if (addr == ""){
        eraseCookie(JUKEBOX_ADDR)
    } else {
        createCookie(JUKEBOX_ADDR, addr);
    }
    window.location.reload();
}


// COOKIES
function createCookie(name, value, days) {
    var expires;

    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = encodeURIComponent(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ')
            c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0)
            return decodeURIComponent(c.substring(nameEQ.length, c.length));
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}
