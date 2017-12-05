$(function() {

    $("#insightful-search-btn").on("click", function(e){
        var query = $('#search-input').val();
        window.location = 'http://localhost:5000/search' + '?q=' + query;
    })

    $("#random-search-btn").on("click", function(e){
        window.location = 'http://localhost:5000/search' + '?q=trump';
    })

    $('#search-form').keypress(function(e){
        if(e.which === 13){//enter key pressed
            $('#insightful-search-btn').click();
            return false;
        }
    });
});
