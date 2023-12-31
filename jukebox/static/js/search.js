var intervalSearch;

$(document).on('keyup', '#search', function(e){
    clearInterval(intervalSearch);
    var q = $('#search').val();
    if (q.length>2){
        intervalSearch = setTimeout(function(){
            doSearch(q);
      }, 1000);
    }
});

function doSearch(q){
    console.log('doSearch:', q);
    $.getJSON('/api/search/' + q, function(data){
        var html = '';
        data.forEach(function(r){
            html += searchItem(r)
        });
        if (html != '') {
            console.log(html);
            $('#search-results').html(html);
            $('#search-results-none').hide();
        } else {
            $('#search-results-none').show();
        }
    });
}


function searchItem(r){
    return `
    <div class="row text-secondary mb-2">
        <div class="col">
            <a class="no-link" href="javascript:;" onclick="playlistSongId(${r.id})">
                <span class="text-light">${r.title}</span><br />
                <small>${r.artist}</small>
            </a>
        </div>
        <div class="col-2">
            <button class="btn btn-md text-light"><i class="bi bi-add"></i></button>
        </div>
    </div>`;
}

