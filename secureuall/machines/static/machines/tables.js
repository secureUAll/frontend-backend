$(document).ready(function () {
    $(document).ready(function () {
        $('#vulnerabilitiesTable').DataTable({
            "lengthMenu": [ 25, 50, 100 ],
        });
        $('#servicesVersions').DataTable({
            "lengthMenu": [ 4, 10, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
        $('#openPorts').DataTable({
            "lengthMenu": [ 4, 10, 25 ],
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
