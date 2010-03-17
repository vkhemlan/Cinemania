/* Script for everyday functions in CineMania */

$(function() {
    /* If there are any error messages, display them swiftly for 4 seconds */
    $("#error_message").slideDown("slow", function() {
        $(this).oneTime(4000, function() {
            $(this).slideUp("slow");
        });
    });
})
