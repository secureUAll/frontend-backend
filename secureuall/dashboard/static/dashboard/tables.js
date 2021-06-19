$(document).ready(function () {
    $(document).ready(function () {
        $('#machinesTable').DataTable({
            "lengthMenu": [ 25, 50, 100 ]
        });
        $('#workersTable').DataTable({
            "lengthMenu": [ 5, 10, 25 ]
        });
        $('#latestChangesTableAddRemoved').DataTable({
            "lengthMenu": [ 10, 15, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
        $('#latestChangesTableUpdates').DataTable({
            "lengthMenu": [ 10, 15, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
        $('#latestChangesTableFixedVulns').DataTable({
            "lengthMenu": [ 10, 15, 25 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
        $('#alertsTable').DataTable({
            "lengthMenu": [ 10 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
    });
});