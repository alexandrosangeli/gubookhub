$(document).ready(function() { 

    $('#search-input').keyup(function() {
        var query;
        query = $(this).val();
        subject = $(this).attr('name');

        $.get(
            '/gubookhub_app/suggest/',
            {'suggestion':query, 'subject':subject},
            function(data){
                $('#course-listing').html(data);
            }
        )
    });

});