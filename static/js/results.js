$(function() {
    $(".subreddit-checkbox").on("click", function(e){
        console.log(e);
        console.log(e.target.id)
        if (e.target.id == 'all'){
            console.log("Deselecting all checkboxes");
            if (e.target.checked){
                console.log('Showing all hits');
            }
            else {
                console.log('Hiding all hits');
            }
        }
        else {
            console.log("Deselecting r/all")
            if (e.target.checked){
                console.log('Filtering posts')
            }
            else {
                console.log('Hiding posts')
            }
        }
  })
});
