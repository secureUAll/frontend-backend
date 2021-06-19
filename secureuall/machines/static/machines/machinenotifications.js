$(document).ready(function() {

    // Get parameters and show notifications if any matching
    const urlParams = new URLSearchParams(window.location.search);

    let title = "";
    let description = "";

    // If removed owner
    if (urlParams.get("removedownersubs")) {
        title = "User disassociated with success";
        description = "The user does not have access to the machine anymore.";
    } else if (urlParams.get("scanlevel")) {
        title = "Scan level changed with success";
        description = "It will be applied in the next scan";
    } else if (urlParams.get("periodicity")) {
        title = "Scan periodicity changed with success";
        description = "It will be applied to schedule the next scan";
    } else if (urlParams.get("scanStatus")) {
        title = "Scan status changed";
        description = "The changes were made with success";
    } else if (urlParams.get("comment")) {
        title = "Comment added";
        description = "Your comment was added to the scan";
    }

    if (title && description) {
        showNotification(
            title,
            description,
            "success",
            "travel_info"
        );
    }

    // If param goto, scroll to element
    if (urlParams.get("goto")) {
        let elem = $("#" + urlParams.get("goto"));
        if (elem.length) {
            elem[0].scrollIntoView({ behavior: 'smooth', block: 'start'});
        }
    }

    // Remove parameter from URL (to avoid duplicate notifications)
    window.history.replaceState({}, document.title, location.protocol + '//' + location.host + location.pathname);

});