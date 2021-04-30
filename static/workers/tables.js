$(document).ready(function () {
    // Find all tables and activate them with datatables
    for(i=1; true; i++) {
        id = "#table" + i;
        if($(id).length == 0) {
            break;
        }
        $(id).DataTable({
            "lengthMenu": [ 4, 10, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
    }
});