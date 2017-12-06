function hideAllHits(hits) {
    console.log('Hiding all hits');
    hits.each(function(idx, div){
        $(div).hide();
    });
}

function showAllHits(hits) {
    console.log('Showing all hits');
    hits.each(function(idx, div){
        $(div).show();
    });
}

function uncheckAllBoxes(){
    console.log("Deselecting all checkboxes");
    var checkboxes = $('#subredditSubmenu').find('input');
    checkboxes.each(function(idx, input){
        if ($(input).prop('id') !== 'all')
            $(input).prop('checked', false);
    });
}

function showHitsBySubreddit(subreddit){
    $(`#hits>div[class*=${subreddit}]`).show();
}

function hideHitsBySubreddit(subreddit){
    $(`#hits>div[class*=${subreddit}]`).hide();
}

$(function() {
    $(".subreddit-checkbox").on("click", function(e){
        var hits = $('#hits').find('div');
        if (e.target.id == 'all'){
            uncheckAllBoxes();
            if (e.target.checked){
                showAllHits(hits);
            }
            else {
                hideAllHits(hits);
            }
        }
        else {
            if (e.target.checked){
                if ($('#all').prop('checked')){
                    $('#all').prop('checked', false);
                    hideAllHits(hits);
                }
                showHitsBySubreddit(e.target.id);
            }
            else {
                hideHitsBySubreddit(e.target.id);            }
        }
  })
});
