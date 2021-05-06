// Remove machine from worker

function removeMachine(machine, worker, dns, ip, adding) {
    const edit = adding!='False';
    const machineName = dns!='null' ? dns : ip;
    if (confirm(`Are you sure you want to remove "${machineName}" from worker "${worker}"?`)) {
        this.event.target.closest("tr").remove();
    }
}