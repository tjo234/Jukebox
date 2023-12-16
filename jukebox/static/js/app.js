// App.js

// Global variable
window.JUKEBOX = {};

// View Handlers
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

// Music Player
$(function() {
    initMusicPlayer();
});
function initMusicPlayer(){
    $.getJSON('/player/initialize', function(){
        refreshPlayerStatus();
        playerWaitForChange();
    });
}
function updateLibrary(){
    $.getJSON('/player/update', function(){
        refreshPlayerStatus()
    });
}
function playerPlayToggle() {
    $.getJSON('/player/control/pause', function(){
        refreshPlayerStatus()
    });
}
function playerMuteToggle() {
    $.getJSON('/player/control/mute', function(){
        refreshPlayerStatus()
    });
}
function playerNextTrack() {
    $.getJSON('/player/control/next', function(){
        refreshPlayerStatus()
    });
}
function playerPrevTrack() {
    $.getJSON('/player/control/previous', function(){
        refreshPlayerStatus()
    });
}
function playerWaitForChange() {
    $.getJSON('/player/idle', function(data){
        console.log('Change received: ' + data)
        // refreshPlayerStatus()
        playerWaitForChange();
    });
}
function refreshPlayerStatus(){
    $.getJSON('/player/status', function(data){
        window.JUKEBOX = data;
        refreshPlayerUI();
    });
}
function refreshPlayerUI(){
    console.log('refreshPlayerUI')

    // Play/Pause Toggle
    if (JUKEBOX.status.state == 'pause') {
        $('.player-btn-play').show();
        $('.player-btn-pause').hide();
    }
    else {
        $('.player-btn-play').hide();
        $('.player-btn-pause').show();
    }

    // Volume Toggle
    if (!JUKEBOX.status.volume) {
        $('.player-btn-volume').hide();
        $('.player-btn-mute').hide();
        $('.player-btn-fixed').show();
    } else if (JUKEBOX.status.volume == 0) {
        $('.player-btn-volume').hide();
        $('.player-btn-mute').show();
        $('.player-btn-fixed').hide();
    } else {
        $('.player-btn-volume').show();
        $('.player-btn-mute').hide();
        $('.player-btn-fixed').hide();
    }
    
    // Track Info
    if ($('#trackid').val() != JUKEBOX.currentsong.id){
        $('#trackid').val(JUKEBOX.currentsong.id);
        $('.player-artist').html(JUKEBOX.currentsong.artist);
        $('.player-album').html(JUKEBOX.currentsong.album);
        $('.player-title').html(JUKEBOX.currentsong.title);
    }

    // Playlist Info
    var playlistHtml = '';
    JUKEBOX.playlist.forEach(function(val){
        playlistHtml += "<li>" + val + "</li>";
    });
    $('#queue').html("<ul class='playlist'>" + playlistHtml + '</ul>');

}


/* Listen in Browser */

// var musicPlayer;
// function initMusicPlayer(){
//   musicPlayer = document.getElementById("player-audio");
//   musicPlayer.addEventListener('ended',function() {
//     togglePlay(false);
//   });
// }

// function playerPlayToggle() {
//   if (musicPlayer.paused) {
//     musicPlayer.play();
//     togglePlay(true);
//   } else {
//     musicPlayer.pause();
//     togglePlay(false);
//   }
// }

// function togglePlay(isPlaying){
//   if (isPlaying){
//     $('.player-btn-play').hide();
//     $('.player-btn-pause').show();
//   } else {
//     $('.player-btn-play').show();
//     $('.player-btn-pause').hide();
//   }
// }

// function playerNextTrack(){
//   var nextId = Number($('#player-id').val())+1;
//   playTrack(nextId);
// }
// function playerPrevTrack(){
//   var nextId = Number($('#player-id').val())-1;
//   playTrack(nextId);
// }

// function playTrack(trackId){
//   console.log('playTrack', trackId)
//   $('#player-id').val(trackId);
//   musicPlayer.src = '/file/'+trackId;
//   musicPlayer.play();
//   togglePlay(true);
// }


// function playerContainerClick(e){
//   console.log('playerContainerClick', e)
// }
// function playerMuteToggle() {
//   console.log('playerMuteToggle', musicPlayer.muted)
//   if (musicPlayer.muted == true) {
//     musicPlayer.muted = false;
//     $('.player-btn-volume').show();
//     $('.player-btn-mute').hide();
//   } else {
//     musicPlayer.muted = true;
//     $('.player-btn-volume').hide();
//     $('.player-btn-mute').show();
//   }
// }

// function showNowPlaying(){
//   console.log('showNowPlaying')
// }