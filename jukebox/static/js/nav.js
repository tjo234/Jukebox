function updateDatabase(rescan){
    console.log('updateDatabase')
    var url = (rescan == true) ? '/api/player/update' : '/api/player/rescan'; 
    $.getJSON(url, function(data){
        console.log('updateDatabase RESP:', data)
    })
}
function waitForDatabaseChange() {
    $.getJSON('/api/player/idle/database', function(data){
        console.log('Database Update' + data)
    });
    $.getJSON('/api/player/idle/library', function(data){
        console.log('Library Update' + data)
    });
}