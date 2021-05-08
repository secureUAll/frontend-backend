$(document).ready(function () {
    // Activate all workers tables
    $(".workersTable").each(function(){
        $(this).DataTable({
            "lengthMenu": [ 5, 10, 25 ],
            "order": [[ 5, "asc" ]]
        });
    });

    // If worker parameter is passed as argument, scroll to that worker
    const urlParams = new URLSearchParams(window.location.search);
    const worker = urlParams.get('worker');
    if(worker!=null) {
        document.querySelector(`#worker${worker}`).scrollIntoView();
    }

});
