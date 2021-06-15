const showNotification = (title, message, color="primary", icon="") => {
    $.notify({
        icon: "now-ui-icons " + icon,
        title: `<b>${title}</b>`,
        message: `${message}`
    }, {
        type: color,
        timer: 8000,
        placement: {
            from: "top",
            align: "center"
        }
    });
}