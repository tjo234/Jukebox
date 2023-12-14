// App.js

/* Default View */
$(function() {
  loadView("home");
  initMusicPlayer();
});

/* View Handlers */ 
addEventListener("hashchange", (event) => {
  const route = window.location.hash.split('?')[0].slice(1);   
  loadView(route);
});

function loadView(route){
  console.log(route)
  $.get('/view/'+route, function(data){
    $('#view-container').html(data);
  })
}

/* Click Handlers */
function scanLibrary(){
  $.getJSON('/api/scan_library', function(data){
    console.log(data)
    window.location.href='/';
  })
}

/* Music PLayer */

var musicPlayer;
function initMusicPlayer(){
  musicPlayer = document.getElementById("player-audio");
  musicPlayer.addEventListener('ended',function() {
    togglePlay(false);
  });
}

function playerPlayToggle() {
  if (musicPlayer.paused) {
    musicPlayer.play();
    togglePlay(true);
  } else {
    musicPlayer.pause();
    togglePlay(false);
  }
}

function togglePlay(isPlaying){
  if (isPlaying){
    $('.player-btn-play').hide();
    $('.player-btn-pause').show();
  } else {
    $('.player-btn-play').show();
    $('.player-btn-pause').hide();
  }
}

function playerNextTrack(){
  var nextId = Number($('#player-id').val())+1;
  playTrack(nextId);
}
function playerPrevTrack(){
  var nextId = Number($('#player-id').val())-1;
  playTrack(nextId);
}

function playTrack(trackId){
  console.log('playTrack', trackId)
  $('#player-id').val(trackId);
  musicPlayer.src = '/file/'+trackId;
  musicPlayer.play();
  togglePlay(true);
}


function playerContainerClick(e){
  console.log('playerContainerClick', e)
}
function playerMuteToggle() {
  console.log('playerMuteToggle', musicPlayer.muted)
  if (musicPlayer.muted == true) {
    musicPlayer.muted = false;
    $('.player-btn-volume').show();
    $('.player-btn-mute').hide();
  } else {
    musicPlayer.muted = true;
    $('.player-btn-volume').hide();
    $('.player-btn-mute').show();
  }
}

function showNowPlaying(){
  console.log('showNowPlaying')
}