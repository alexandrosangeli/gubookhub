$(document).ready(function() { 

    $('#search-input').keyup(function() {
        var query;
        query = $(this).val();

        $.get(
            '/gubookhub_app/suggest/',
            {'suggestion':query},
            function(data){
                $('#course-listing').html(data);
            }
        )
    });

});