/*
    JSON Highlighting
    Based on https://ourcodeworld.com/articles/read/112/how-to-pretty-print-beautify-a-json-string
*/
function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}
/*
    JSON Highlighting END
*/

$(document).ready(function () {
    // Initialize table
    var table = $("#scansTable").DataTable({
        "lengthMenu": [ 25, 50, 100 ],
        "order": [[ 0, "desc" ]]
    });

    // Create listener for user click
    table.on('click', 'tr', function() {
        // Get row and extract log id
        var row = table.row(this).data(); // Array [ "April 15, 2021<span class=\"d-none\">3</span>", "192.168.0.12" ]
        var id = row[0].split("\">")[1].split("<")[0];
        console.log(id);
        // Start loading...
        $(".spinner-grow").removeClass("d-none");
        $("#log").hide();
        // Get log from API
        fetch('/machines/logs/' + id)
            .then(res => res.json())
            .then(function(response) {
                // If error, display notification
                if ('error' in response) {
                    showNotification(
                        "Error!",
                        "There was an error obtaining the requested log, please try again.",
                        "danger",
                        "ui-2_settings-90"
                    );
                // Else, render log
                } else {
                    var log = response[0]['fields']['log'];
                    console.log("GOTTT", response);
                    // Show JSON beautified, if error parsing show raw and notify
                    try {
                        var logObj = JSON.parse(log);
                        var logIndent = JSON.stringify(logObj, null, 4);
                        $("#log").html(syntaxHighlight(logIndent));
                    } catch (error) { // if error
                        $("#log").html(log);
                        showNotification(
                            "There was an error processing the log!",
                            "The log appears to have an invalid JSON structure. Because of that we can not display it beautified. You are shown the raw version.",
                            "danger",
                            "travel_info"
                        );
                    }
                }
                // Finish loading...
                $(".spinner-grow").addClass("d-none");
                $("#log").show();
            });
    });


});