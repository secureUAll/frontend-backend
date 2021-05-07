from django import forms
from django.forms.utils import ErrorList
import re

from .validators import *
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
        if not super(MachineWorkerBatchInputForm, self).is_valid():
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
            if not (validate_ip(m) or validate_dns(m)):
                continue
            # Create Machine objects
            mobj = Machine(
                ip=m if validate_ip(m) else None,
                dns=m if validate_dns(m) else None
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


class MachineForm(forms.Form):
    ip = forms.CharField(
        max_length=15,
        required=False,
        validators=[validate_ip],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="IP address"
    )
    dns = forms.CharField(
        max_length=255,
        required=False,
        validators=[validate_dns],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label = "DNS"
    )
    location = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    scanLevel = forms.ChoiceField(choices=Machine.scanLevelOps, required=False, label="Scan level")
    periodicity = forms.ChoiceField(choices=Machine.periodicityOps, required=False)
    # Control variables
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        if not validate_ip(ip):
            raise ValidationError('IP address is not valid.')
        return ip

    def clean_dns(self):
        dns = self.cleaned_data['dns']
        if not validate_dns(dns):
            raise ValidationError('DNS name is not valid.')
        return dns

    def clean(self):
        cleaned_data = super(MachineForm, self).clean()
        # If does not have IP or DNS, throw error
        if 'ip' in self.cleaned_data and self.cleaned_data['ip']:
            return cleaned_data
        if 'dns' in self.cleaned_data and self.cleaned_data['dns']:
            return cleaned_data

        for k in ['dns', 'ip']:
            if k not in self._errors:
                self._errors[k] = ErrorList()
            self._errors[k].append('A machine must have an IP and/or DNS name.')
        return cleaned_data

    def is_valid(self):
        # Validate with default validator
        if not super(MachineForm, self).is_valid():
            return False
        # Add extra attributes
        dbquery = Machine.exists(self.cleaned_data['ip'], self.cleaned_data['dns'])
        if dbquery.exists():
            self.cleaned_data['id'] = dbquery.first().id
        return True







