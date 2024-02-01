/* 
-------------------------------------------------------------------------------

    PLAYER.JS
    API Proxy for the MPD API controls.
    Views call initPlayer with a callback function.
    Whenever MPD state changes the idle function will trigger a UI refresh.
    Data is shared across views using window.JUKEBOX

-------------------------------------------------------------------------------
*/
window.JUKEBOX = {};

$(document).keydown(function(e){
    console.log( "Handler for `keypress` called.", e.which, e.metaKey);
    
    if (e.which == 32) {
        playerPlayToggle();
        e.preventDefault();
    } else if (e.metaKey && e.which == 39) {
        playerNextTrack();
        e.preventDefault();
    } else if (e.metaKey && e.which == 37) {
        playerPrevTrack();
        e.preventDefault();
    } else if (e.metaKey && e.which == 40) {
        lowerVolume();
        e.preventDefault();
    } else if (e.metaKey && e.which == 38) {
        raiseVolume();
        e.preventDefault();
    }
});

function initPlayer(callback){
    refreshPlayerStatus('init', callback);
    playerWaitForChange(callback);
}
function playerWaitForChange(callback) {
    $.getJSON('/api/player/idle', function(evt){
        console.log('Change received: ' + evt)
        refreshPlayerStatus(evt, callback)
        playerWaitForChange(callback);
    });
}
function refreshPlayerStatus(evt, callback){
    $.getJSON('/api/player/status', function(data){
        window.JUKEBOX = data;
    })
    .fail(function() { 
        console.log("Could not get JUKEBOX status."); 
        window.JUKEBOX = {};
    })
    .always(function() { 
        callback(evt);
    });
}


/* 
-------------------------------------------------------------------------------

    MPD COMMANDS
    The UI is already listening for these updates in refreshPlayerUI()

-------------------------------------------------------------------------------
*/
function updateDatabase(rescan){
    var url = (rescan == true) ? '/api/player/rescan' : '/api/player/update'; 
    $.getJSON(url);
}
function cacheAlbumCovers(){
    console.log('cacheAlbumCovers')
    $.getJSON('/api/cache_album_covers');
}
function reCacheAlbumCovers(){
    console.log('reCacheAlbumCovers')
    $.getJSON('/api/recache_album_covers');
}
function toggleOutput(id){
    $.getJSON(`/api/player/toggleoutput/${id}`, function(){});
}
function playerSeek(obj){
    $.getJSON('/api/player/seek/'+$(obj).val(), function(){});
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
function changeVolume(obj) {
    v = $(obj).val();
    $.getJSON('/api/player/volume/'+v, function(){});
}
function lowerVolume() {
    v = parseInt(JUKEBOX.status.volume * 0.9);
    $('.volume-bar').val(v);
    $.getJSON('/api/player/volume/' + v, function(){});
}
function raiseVolume() {
    v = parseInt(JUKEBOX.status.volume * 1.1);
    if (v > 100) v = 100;
    $('.volume-bar').val(v);
    $.getJSON('/api/player/volume/' + v, function(){});
}
function playerNextTrack() {
    $.getJSON('/api/player/control/next', function(){});
}
function playerPrevTrack() {
    $.getJSON('/api/player/control/previous', function(){});
}
function playerRepeat() {
    console.log('playerRepeat')
    $.getJSON('/api/player/control/repeat', function(){});
}
function playerShuffle() {
    console.log('playerShuffle')
    $.getJSON('/api/player/control/random', function(){});
}
function saveQueueAsPlaylist(){
    var name = prompt('Save Playlist As:');
    if (name == '') {
        alert('Please enter a name!')
        return null;
    }
    $.getJSON('/api/playlist/save/?playlist='+name, function(){
        $.get('/view/desktop/playlists', function(data){
            $('#playlists-nav').html(data);
        });
        window.location.href = '#playlist?playlist=' + name;
    });
}
function clearPlaylist(){
    $.getJSON('/api/playlist/clear/', function(){});
}
function playlistSongId(songId) {
    $.getJSON('/api/playlist/playid/'+songId, function(){});
}
function deleteFromQueue(songId) {
    $.getJSON('/api/playlist/deleteid/'+songId, function(){});
}
function playAlbum(a){
     $.getJSON('/api/playlist/queue/album/?album='+a, function(){});
}
function playArtist(a){
     $.getJSON('/api/playlist/queue/artist/?artist='+a, function(){});
}
function queueSong(file){
     $.getJSON('/api/playlist/add/?file='+file, function(){});
}
function playAlbumTrack(album, track){
     $.getJSON('/api/album/play/?album='+album+'&track='+track, function(){});
}
function playPlaylist(p){
    $.getJSON('/api/playlist/load/?playlist='+p, function(){});
}
function playPlaylistTrack(p,track){
    $.getJSON('/api/playlist/track/?playlist='+p+'&track='+track, function(){});
}
function playerFindAdd(tag, what){
    $.getJSON(`/api/playlist/findadd/${tag}/${what}`, function(){
        $('#player-full').modal('show');
    });
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
function seekUpdate(){
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



