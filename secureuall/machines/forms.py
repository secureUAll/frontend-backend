from django import forms
import re

from .models import Machine, MachineWorker

# Global variables
batchInputRegex = r",|;|\n"


class MachineWorkerBatchInputForm(forms.Form):
    """
    Get batch input for machine names to associate with worker
    -- Parameters
    batch               String                          Raw text with machine names separated by one of batchInputRegex symbols
    -- Returns (in self.cleaned_data)
    machines            machines.models.Machine[]
    ignored             int                             Number of invalid machines in input
    alreadyAssociated   int                             Number of machines that were already associated with worker
    edit                bool                            Does any machine match any at the db?
    """
    batch = forms.CharField(
        label="Machines list",
        widget=forms.Textarea(attrs={'placeholder': 'Write your list here', 'class': 'form-control'})
    )

    def validate_custom(self, worker):
        # Validate with default validator
        if not self.is_valid():
            return False
        # Start variables
        self.cleaned_data['machines'] = []
        self.cleaned_data['alreadyAssociated'] = 0
        self.cleaned_data['edit'] = False
        # Split input by batchInputRegex symbols
        original = [m.strip() for m in re.split(batchInputRegex, self.cleaned_data['batch'].strip())]
        # For each entry
        for m in original:
            # If m is not a valid DNS nor IP, ignore...
            if not (Machine.is_ip(m) or Machine.is_dns(m)):
                continue
            # Create Machine objects
            mobj = Machine(
                ip=m if Machine.is_ip(m) else None,
                dns=m if Machine.is_dns(m) else None
            )
            # Check if already exists in the database
            dbquery = Machine.exists(mobj.ip, mobj.dns)
            if dbquery.exists():
                mobj = dbquery.first()
                mobj.edit = True
                self.cleaned_data['edit'] = True
                if MachineWorker.objects.filter(machine=mobj, worker=worker).exists():
                    mobj.alreadyAssociated = True
                    self.cleaned_data['alreadyAssociated'] += 1
            self.cleaned_data['machines'].append(mobj)
        # Update global variables
        self.cleaned_data['ignored'] = len(original) - len(self.cleaned_data['machines'])
        # Check if any machine is valid
        return len(self.cleaned_data['machines'])>0
