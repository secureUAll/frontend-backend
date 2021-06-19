$(document).ready(function() {

    // Datatables
    $('#requestsTable').DataTable({
        "lengthMenu": [ 25, 50, 100 ],
    });

    // Fill request modal when click on status change button
    $('#changeRequestStatusModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget) // Button that triggered the modal
      // Extract info from data-* attributes
      var approve = button.data('approve');
      var user = button.data('user');
      var machines = button.data('machines');
      var id = button.data('id');
      machines = JSON.parse(machines.replaceAll("'", "\""));
      // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
      var modal = $(this);
      modal.find('#user').text(user);
      modal.find('#machines').html(machines.join('<br/>'));
      modal.find('#requestid').val(id);
      if (approve=="True") {
        modal.find('#approveRequest').click();
      } else {
        modal.find('#denyRequest').click();
      }
    });

    // Send form (async)
    $("#changeRequestStatusSubmit").click(() => {
        $.ajax({
           type: 'POST',
           url: '#',
           data: $('#changeRequestStatusForm').serialize(),
           success: (data) => {
                requestResponse(data, 200);
           },
           error: (request, status, error) => {
                requestResponse(request.responseText, status);
           }
        });
    });

    const requestResponse = (data, status) => {
        let message = "It was not possible to make the change status request. Try again.";
        if (data!="") {
            let obj = {};
            // Convert data to object, if necessary
            if ((typeof data)=="string") {
                obj = JSON.parse(data);
            } else {
                obj = data;
            }

            // Compute response based on data
            if (status!=200 && 'error' in obj) {
                message = obj['error'];
            } else if (status==200 && 'request' in obj && 'approve' in obj) {
                message = "The request was ";
                message += obj['approve'] ? "approved!" : "rejected!";
                // On success, remove table row for approval
                $("#requestRow" + obj['request']).remove();
                // Close modal
                $('#changeRequestStatusModal').modal('hide');
            }

            console.log("RESPONSE");
            console.log(obj);
        }

        // Show notification
        showNotification(
            status==200 ? "Success" : "Error!",
            message,
            status==200 ? "primary" : "danger",
            status==200 ? "travel_info" : "ui-2_settings-90"
        );
    }

});