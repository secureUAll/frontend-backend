const showNotification = (from, align) => {
    color = 'primary';

    $.notify({
        icon: "now-ui-icons ui-1_bell-53",
        message: "Welcome to <b>Now Ui Dashboard</b> - a beautiful freebie for every web developer."

    }, {
        type: color,
        timer: 8000,
        placement: {
            from: from,
            align: align
        }
    });
}