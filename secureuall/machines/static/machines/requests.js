$(document).ready(function() {

    // DEBUG
    // $(".tooltip-test")[0].click();

    // Fill request modal when click on status change button
    $('#changeRequestStatusModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget) // Button that triggered the modal
      // Extract info from data-* attributes
      var approve = button.data('approve');
      var user = button.data('user');
      var machines = button.data('machines');
      machines = JSON.parse(machines.replaceAll("'", "\""));
      // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
      var modal = $(this);
      modal.find('#user').text(user);
      modal.find('#machines').html(machines.join('<br/>'));
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
            console.log("SUCCESS");
            console.log(data);
           },
        });
    });

});