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
    } else if (e.metaKey && e.which == 39) {
        playerNextTrack()
    } else if (e.metaKey && e.which == 37) {
        playerPrevTrack()
    } else if (e.metaKey && e.which == 40) {
        lowerVolume();
    } else if (e.metaKey && e.which == 38) {
        raiseVolume();
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
function changeVolume() {
    v = $('#volume-bar').val();
    $.getJSON('/api/player/volume/'+v, function(){});
}
function lowerVolume() {
    v = $('#volume-bar').val() * 0.9;
    $('#volume-bar').val(v);
    $.getJSON('/api/player/volume/' + v, function(){});
}
function raiseVolume() {
    v = $('#volume-bar').val() * 1.1;
    if (v > 100) v = 100;
    $('#volume-bar').val(v);
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
    if (name == '') return;
    $.getJSON('/api/playlist/save/?playlist='+name, function(){});
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
function playPlaylist(p){
    $.getJSON('/api/playlist/load/?playlist='+p, function(){});
}
function playerFindAdd(tag, what){
    $.getJSON(`/api/playlist/findadd/${tag}/${what}`, function(){
        $('#player-full').modal('show');
    });
}