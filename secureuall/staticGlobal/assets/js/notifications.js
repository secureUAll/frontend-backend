const showNotification = (title, message, color="primary", icon="") => {
    $.notify({
        icon: "now-ui-icons " + icon,
        message: `<b>${title}</b><br/>${message}`

    }, {
        type: color,
        timer: 8000,
        placement: {
            from: "top",
            align: "center"
        }
    });
}