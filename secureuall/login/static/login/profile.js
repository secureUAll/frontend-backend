$(document).ready(function() {

    $("#notificationsForm").on("submit", () => {
        // Validate that user has at least one notification way selected
        let selected = false;
        $('#notificationsForm input[type=checkbox]').each((i, el) => {
            selected = (selected || $(el).prop("checked"));
        });
        // If not selected, alert user!
        if (!selected) {
            showNotification(
                "Error!",
                "You need to select at least one notification type.",
                "danger",
                "ui-2_settings-90"
            );
        }
        return selected;
    })

});
