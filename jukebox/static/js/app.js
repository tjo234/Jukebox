// App.js

// Global variables
window.JUKEBOX = {};


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
    $('#view-container').html('');
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
    playerWaitForChange()
    $.getJSON('/api/player/initialize', function(data){
        refreshPlayerStatus();
    });
}
function playerWaitForChange() {
    $.getJSON('/api/player/idle', function(data){
        console.log('Change received: ' + data)
        refreshPlayerStatus()
        playerWaitForChange();
    });
}

function secondsToElapsed(s){
    var str_elapsed;
    if (s >= 60*60) {
        str_elapsed = new Date(s * 1000).toISOString().slice(11, 19);    
    } {
        str_elapsed = new Date(s * 1000).toISOString().slice(14, 19);    
    }
    return str_elapsed;
}
var intervalPlayerTick;
var elapsed;
function seekUpdate(){
    console.log('seekUpdate')
    clearInterval(intervalPlayerTick);
    if (JUKEBOX.status.state == 'play') {
        $('#player-duration').html(JUKEBOX.status.str_duration);
        $('#player-elapsed').html(JUKEBOX.status.str_elapsed);
        $('#player-seek').attr('min', 0);
        $('#player-seek').attr('max', JUKEBOX.status.duration);
        $('#player-seek').val(JUKEBOX.status.elapsed);
        elapsed = Number.parseInt(JUKEBOX.status.elapsed);
        intervalPlayerTick = setInterval(function(){
            console.log('tick')
            elapsed++;
            $('#player-seek').val(elapsed);
            $('#player-elapsed').html(secondsToElapsed(elapsed));
        }, 1000);
    } else if (JUKEBOX.status.state == 'stop') {
        $('#player-duration').html("0:00");
        $('#player-elapsed').html("0:00");
        $('#player-seek').attr('min', 0);
        $('#player-seek').attr('max', 100);
        $('#player-seek').val(0);
        elapsed = 0;
    }
}

function refreshPlayerStatus(){
    $.getJSON('/api/player/status', function(data){
        window.JUKEBOX = data;
        refreshPlayerUI();
    });
}
function refreshPlayerUI(){
    console.log('refreshPlayerUI');

    seekUpdate();

    // Album Cover 
    $('#img-album').attr('src', JUKEBOX.cover);

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
    $.getJSON(`/api/player/toggleoutput/${id}`, function(){});
}
/* 
-------------------------------------------------------------------------------

    MPD COMMANDS
    The UI is already listening for these updates in refreshPlayerUI()

-------------------------------------------------------------------------------
*/
function playerSeek(){
    $.getJSON('/api/player/seek/'+$('#player-seek').val(), function(){});
}
function updateLibrary(){
    $.getJSON('/api/player/update', function(){});
}
function playerPlayToggle() {
    if (JUKEBOX.status.state == 'play') {
        $.getJSON('/api/player/control/pause', function(){});
    } else {
        $.getJSON('/api/player/control/play', function(){});
    }
}
function playerMuteToggle() {
    $.getJSON('/api/player/control/mute', function(){});
}
function playerNextTrack() {
    $.getJSON('/api/player/control/next', function(){});
}
function playerPrevTrack() {
    $.getJSON('/api/player/control/previous', function(){});
}
function playerRepeat() {
    $.getJSON('/api/player/control/repeat', function(){});
}
function playerShuffle() {
    $.getJSON('/api/player/control/random', function(){});
}