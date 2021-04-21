$(document).ready(function () {
    $(document).ready(function () {
        $('#machinesTable').DataTable({
            "lengthMenu": [ 5, 10, 25 ]
        });
        $('#workersTable').DataTable({
            "lengthMenu": [ 5, 10, 25 ]
        });
        $('#latestChangesTableAddRemoved').DataTable({
            "lengthMenu": [ 4, 10, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
        $('#latestChangesTableUpdates').DataTable({
            "lengthMenu": [ 4, 10, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
        $('#latestChangesTableFixedVulns').DataTable({
            "lengthMenu": [ 4, 10, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
    });
});