
$(document).ready(function () {
// Bind a click event listener to the upvote button
$('.upvote').click(function (e) {

    e.preventDefault();
    const postId = $(this).data('post-id');
    const voteCountElem = $('.votes-count[data-post-id=' + postId + ']');

    // Send a POST request to the upvote view using AJAX
    $.ajax({
    type: 'POST',
    url: "{% url 'post:upvote' 0 %}".replace('0', postId),
    data: { 'post_id': postId },
    headers: { 'X-CSRFToken': '{{ csrf_token }}' },
    success: function (response) {

        const votes = $("#vote_count" + postId).text()




        if ($('.downvote[data-post-id=' + postId + '] .material-icons').hasClass('text-danger')) {
        if (parseInt(votes) == -1) {
            const newVotes = parseInt(votes) + 2;
            $("#vote_count" + postId).text(newVotes)
        }
        else {
            const newVotes = parseInt(votes) + 1;
            $("#vote_count" + postId).text(newVotes)
        }

        ;
        $('.downvote[data-post-id=' + postId + '] .material-icons').removeClass('text-danger').addClass('text-muted');
        $('.upvote[data-post-id=' + postId + '] .material-icons').removeClass('text-muted').addClass('text-danger');
        }
        else if ($('.upvote[data-post-id=' + postId + '] .material-icons').hasClass('text-danger')) {
        const newVotes = parseInt(votes) - 1;
        $("#vote_count" + postId).text(newVotes);
        $('.upvote[data-post-id=' + postId + '] .material-icons').removeClass('text-danger').addClass('text-muted');

        }
        else {
        const newVotes = parseInt(votes) + 1;
        $("#vote_count" + postId).text(newVotes);
        $('.upvote[data-post-id=' + postId + '] .material-icons').removeClass('text-muted').addClass('text-danger');
        }
    },
    error: function (xhr, status, error) {
        // Handle errors
    }
    });
});





$('.downvote').click(function (e) {

    e.preventDefault();
    const postId = $(this).data('post-id');
    const voteCountElem = $('.votes-count[data-post-id=' + postId + ']');

    
    $.ajax({
    type: 'POST',
    url: "{% url 'post:downvote' 0 %}".replace('0', postId),
    data: { 'post_id': postId },
    headers: { 'X-CSRFToken': '{{ csrf_token }}' },
    success: function (response) {

        const votes = $("#vote_count" + postId).text()




        if ($('.upvote[data-post-id=' + postId + '] .material-icons').hasClass('text-danger')) {
        if (parseInt(votes) == 1) {
            const newVotes = parseInt(votes) - 2;
            $("#vote_count" + postId).text(newVotes)
        }
        else {
            const newVotes = parseInt(votes) - 1;
            $("#vote_count" + postId).text(newVotes)
        }

        
        $('.upvote[data-post-id=' + postId + '] .material-icons').removeClass('text-danger').addClass('text-muted');
        $('.downvote[data-post-id=' + postId + '] .material-icons').removeClass('text-muted').addClass('text-danger');
        }
        else if ($('.downvote[data-post-id=' + postId + '] .material-icons').hasClass('text-danger')) {
        const newVotes = parseInt(votes) + 1;
        $("#vote_count" + postId).text(newVotes);
        $('.downvote[data-post-id=' + postId + '] .material-icons').removeClass('text-danger').addClass('text-muted');

        }
        else {
        const newVotes = parseInt(votes) - 1;
        $("#vote_count" + postId).text(newVotes);
        $('.downvote[data-post-id=' + postId + '] .material-icons').removeClass('text-muted').addClass('text-danger');
        }
    },
    error: function (xhr, status, error) {
        // Handle errors
    }
    });
});






});



