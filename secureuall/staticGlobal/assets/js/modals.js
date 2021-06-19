$(document).ready(function() {
    $('.modal').each((i, m) => {
        $("#"+m.id).appendTo("body");
    });
});