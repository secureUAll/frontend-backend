$(document).ready(function () {
    $(document).ready(function () {
        // Activate all workers tables
        $(".workersTable").each(function(){
            $(this).DataTable({
                "lengthMenu": [ 5, 10, 25 ],
                "order": [[ 3, "asc" ]]
            });
        });

    })
});