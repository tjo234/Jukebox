// App.js

/* Default View */
$(function() {
  loadView("home");
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
  })
}

