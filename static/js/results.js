function hideAllHits(hits) {
    console.log('Hiding all hits');
    hits.each(function(idx, div){
        console.log(idx);
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

function uncheckOtherSortBoxes(checkedId) {
    var $checkboxes = $('#sortSubmenu').find('input');
    $checkboxes.each(function(idx, input){
        if ( $(input).prop('id') !== checkedId)
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
        var hits = $('#hits').find('div.hit');
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
                hideHitsBySubreddit(e.target.id);
            }
        }
    });

    $('#sortSubmenu>label>input').on('click', function(e){
        let sortAttr = e.target.id.split('-')[2];
        let sortAscending = false;
        console.log(`Sorting on ${sortAttr}`);
        uncheckOtherSortBoxes(e.target.id);
        let $hits = $(`#hits>div[class*=hit`);
        $hits.sort(function(a, b){
            let an = a.getAttribute(`data-${sortAttr}`), bn = b.getAttribute(`data-${sortAttr}`);
            let mult = 1;
            if (!sortAscending) mult = -1;
            if (an > bn)
                return 1*mult;
            if (an < bn)
                return -1*mult;
            return 0;
        });


        $hits.detach().appendTo($('#hits'));
        $hits = $(`#hits>div[class*=hit`);
        $hits.each(function(idx, div){
            console.log($(div).attr(`data-${sortAttr}`));
        });
    });



});
