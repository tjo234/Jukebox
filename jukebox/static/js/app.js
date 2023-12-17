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
    initPlayer();
});
function initPlayer(){
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
        //refreshPlayerStatus()
    });
}
function playerMuteToggle() {
    $.getJSON('/player/control/mute', function(){
        //refreshPlayerStatus()
    });
}
function playerNextTrack() {
    $.getJSON('/player/control/next', function(){
        //refreshPlayerStatus()
    });
}
function playerPrevTrack() {
    $.getJSON('/player/control/previous', function(){
        //refreshPlayerStatus()
    });
}
function playerRepeat() {
    $.getJSON('/player/control/repeat', function(){
        //refreshPlayerStatus()
    });
}
function playerShuffle() {
    $.getJSON('/player/control/random', function(){
        //refreshPlayerStatus()
    });
}
function playerWaitForChange() {
    $.getJSON('/player/idle', function(data){
        console.log('Change received: ' + data)
        refreshPlayerStatus()
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
    if (JUKEBOX.status.state == 'play') {
        console.log('Playing');
        $('.player-btn-play').addClass('hidden');
        $('.player-btn-pause').removeClass('hidden');
    }
    else {
        console.log('Not Playing')
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
    if ($('#trackid').val() != JUKEBOX.currentsong.id){
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