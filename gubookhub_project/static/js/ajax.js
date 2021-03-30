$(document).ready(function () {

    $('#course-search-input').keyup(function () {
        var query;
        query = $(this).val();
        subject = $(this).attr('name');

        $.get(
            '/gubookhub_app/suggest_courses/',
            { 'suggestion': query, 'subject': subject },
            function (data) {
                $('#course-listing').html(data);
            }
        )
    });

    $('#subject-search-input').keyup(function () {
        var query;
        query = $(this).val();

        $.get(
            '/gubookhub_app/suggest_subjects/',
            { 'suggestion': query,},
            function (data) {
                $('#subject-listing').html(data);
            }
        )
    });

});