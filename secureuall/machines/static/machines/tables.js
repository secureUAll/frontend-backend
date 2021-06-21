$(document).ready(function () {
    $(document).ready(function () {
        $('#servicesVersions').DataTable({
            "lengthMenu": [ 4, 10, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
        $('#openPorts').DataTable({
            "lengthMenu": [ 10, 10, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });

        $('#vulnComments').DataTable({
            "lengthMenu": [ 4, 10, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": true
        });
    });
});
