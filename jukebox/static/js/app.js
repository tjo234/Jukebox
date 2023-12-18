// App.js

// Global variables
var JUKEBOX = {};
var intervalPlayerTick;

/*
-------------------------------------------------------------------------------

    AJAX View Handlers

-------------------------------------------------------------------------------
*/
$(function() {
    loadView("home");
});
addEventListener("hashchange", (event) => {
    const route = window.location.hash.split('?')[0].slice(1);   
    loadView(route);
});
function loadView(route){
    console.log(route)
    $.get('/view/'+route, function(data){
        $('#view-container').html(data);
    });
}

/*
-------------------------------------------------------------------------------

    Music Player Controls

-------------------------------------------------------------------------------
*/


$(function() {
    initPlayer();
});
function initPlayer(){
    $.getJSON('/player/initialize', function(){
        refreshPlayerStatus();
        playerWaitForChange();
    });
}
function playerWaitForChange() {
    $.getJSON('/player/idle', function(data){
        console.log('Change received: ' + data)
        refreshPlayerStatus()
        playerWaitForChange();
    });
}
function seekUpdate(){
    if (JUKEBOX.status.state == 'play') {
        $('#player-duration').html(JUKEBOX.status.str_duration);
        $('#player-elapsed').html(JUKEBOX.status.str_elapsed);
        $('#player-seek').attr('min', 0);
        $('#player-seek').attr('max', JUKEBOX.status.duration);
        $('#player-seek').val(JUKEBOX.status.elapsed);
    } else {
        $('#player-duration').html("0:00");
        $('#player-elapsed').html("0:00");
        $('#player-seek').attr('min', 0);
        $('#player-seek').attr('max', 100);
        $('#player-seek').val(0);
    }
}
function playerTick(){
    $.getJSON('/player/status', function(data){
        console.log('tick', data.status.elapsed)
        JUKEBOX = data;
        seekUpdate();
    });
}
function refreshPlayerStatus(){
    $.getJSON('/player/status', function(data){
        JUKEBOX = data;
        refreshPlayerUI();
    });
}
function refreshPlayerUI(){
    console.log('refreshPlayerUI');

    seekUpdate();
    clearInterval(intervalPlayerTick);
    intervalPlayerTick = setInterval(function(){
        playerTick()
    }, 1000);

    // Album Cover 
    if (JUKEBOX.cover) {
        $('#img-album').attr('src', 'player/cover');
    } else {
        $('#img-album').attr('src', '/static/img/album.png');
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
        $('#trackid').val('');
        $('.player-artist').html('&nbsp;');
        $('.player-album').html('&nbsp;');
        $('.player-title').html('&nbsp;');
    }
    else if ($('#trackid').val() != JUKEBOX.currentsong.id){
        $('#trackid').val(JUKEBOX.currentsong.id);
        $('.player-artist').html(JUKEBOX.currentsong.artist);
        $('.player-album').html(JUKEBOX.currentsong.album);
        $('.player-title').html(JUKEBOX.currentsong.title);
    }

    // Playlist Info
    var playlistHtml = '';
    if(JUKEBOX.playlist) {
        JUKEBOX.playlist.forEach(function(val){
            playlistHtml += "<li>" + val + "</li>";
        });
    }
    $('#queue').html("<ul class='playlist'>" + playlistHtml + '</ul>');

}

/* 
-------------------------------------------------------------------------------

    AUDIO COMMANDS
    The UI is already listening for these updates in refreshPlayerUI()

-------------------------------------------------------------------------------
*/
function toggleOutput(id){
    $.getJSON(`/player/toggleoutput/${id}`, function(){});
}
/* 
-------------------------------------------------------------------------------

    MPD COMMANDS
    The UI is already listening for these updates in refreshPlayerUI()

-------------------------------------------------------------------------------
*/
function playerSeek(){
    $.getJSON('/player/seek/'+$('#player-seek').val(), function(){});
}
function updateLibrary(){
    $.getJSON('/player/update', function(){});
}
function playerPlayToggle() {
    if (JUKEBOX.status.state == 'play') {
        $.getJSON('/player/control/pause', function(){});
    } else {
        $.getJSON('/player/control/play', function(){});
    }
}
function playerMuteToggle() {
    $.getJSON('/player/control/mute', function(){});
}
function playerNextTrack() {
    $.getJSON('/player/control/next', function(){});
}
function playerPrevTrack() {
    $.getJSON('/player/control/previous', function(){});
}
function playerRepeat() {
    $.getJSON('/player/control/repeat', function(){});
}
function playerShuffle() {
    $.getJSON('/player/control/random', function(){});
}