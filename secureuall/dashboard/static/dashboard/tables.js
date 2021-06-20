$(document).ready(function () {
    $(document).ready(function () {
        // On filter

        $('#workersTable').DataTable({
            "lengthMenu": [ 5, 10, 25 ]
        });
        $('#latestChangesTableAddRemoved').DataTable({
            "lengthMenu": [ 5 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
        $('#latestChangesTableUpdates').DataTable({
            "lengthMenu": [ 5 ],
            "searching": false,
            "lengthChange": false,
            "ordering": false
        });
        $('#latestChangesTableFixedVulns').DataTable({
            "lengthMenu": [ 5 ],
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