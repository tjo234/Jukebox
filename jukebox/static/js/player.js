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
    v = $('#volume-bar').val()
    $.getJSON('/api/player/volume/'+v, function(){});
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



function playlistSongId(songId) {
    $.getJSON('/api/playlist/playid/'+songId, function(){});
}
function playAlbum(a){
    console.log('playAlbum', a)
     $.getJSON('/api/playlist/queue/album/?album='+a, function(){});
}
function playArtist(a){
    console.log('playArtist', a)
     $.getJSON('/api/playlist/queue/artist/'+a, function(){});
}
function playPlaylist(p){
    console.log('playPlaylist', p)
    $.getJSON('/api/playlist/load/'+p, function(){});
}
function playerFindAdd(tag, what){
    $.getJSON(`/api/playlist/findadd/${tag}/${what}`, function(){
        $('#player-full').modal('show');
    });
}