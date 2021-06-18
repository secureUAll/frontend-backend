$(document).ready(function () {
    // Activate all workers tables
    $(".workersTable").each(function(){
        $(this).DataTable({
            "lengthMenu": [ 5, 10, 25 ],
            "order": [[ 5, "asc" ]]
        });
    });

    // If worker parameter is passed as argument, scroll to that worker
    const urlParams = new URLSearchParams(window.location.search);
    const worker = urlParams.get('worker');
    if(worker!=null) {
        document.querySelector(`#worker${worker}`).scrollIntoView();
    }

    // Make worker name editable
    $.fn.editable.defaults.mode = 'inline';
    $(".workerTitle").editable({
        type: 'text',
        params: {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(response, newValue) {
            console.log("SUCCESS", response);
            return {'newValue': response[0]['fields']['name']};
        },
        error: function(response, newValue) {
            showNotification(
                "Error!",
                "There was an error changing the worker name. Please try again.",
                "danger",
                "ui-2_settings-90"
            );
            console.log("ERROR changing worker name:", response);
        },
        validate: function(value) {
            if(value.trim().length>12) {
                showNotification(
                    "Invalid name!",
                    "The worker name must have less that 13 characters.",
                    "danger",
                    "ui-2_settings-90"
                );
                return {newValue: ''}
            } else if (value.trim().length==0) {
                return {newValue: ''}
            }
        }
    });

    // Worker table accordion changing toggler text on toggle
    $(".collapse").on('show.bs.collapse', function() {
        $(this).parent().find("button[data-toggle=collapse]").html("<i class=\"now-ui-icons ui-1_simple-delete mr-2\"></i> Hide hosts")
    });

    $(".collapse").on('hide.bs.collapse', function() {
        $(this).parent().find("button[data-toggle=collapse]").html("<i class=\"now-ui-icons tech_laptop mr-2\"></i> See hosts")
    });

});
