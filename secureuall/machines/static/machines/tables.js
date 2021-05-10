$(document).ready(function () {
    $(document).ready(function () {
        $('#vulnerabilitiesTable').DataTable({
            "lengthMenu": [ 5, 10, 25 ],
            "searching": false
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
    });
});
