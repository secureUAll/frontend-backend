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
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="This is only for your information. Does not interfere with the system."
    )
    scanLevel = forms.ChoiceField(
        choices=Machine.scanLevelOps,
        required=False,
        label="Scan level",
        help_text="The higher the level, the more intrusive the scanning. Find more on documentation."
    )
    periodicity = forms.ChoiceField(choices=Machine.periodicityOps, required=False)
    # Control variables
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        if ip and not validate_ip(ip):
            raise ValidationError('IP address is not valid.', params={'ip', ip})
        return ip

    def clean_dns(self):
        dns = self.cleaned_data['dns']
        if dns and not validate_dns(dns):
            raise ValidationError('DNS name is not valid.', params={'dns', dns})
        return dns

    def clean(self):
        cleaned_data = super(MachineForm, self).clean()
        # If does not have IP or DNS, throw error
        if not(('ip' in self.cleaned_data and self.cleaned_data['ip']) or ('dns' in self.cleaned_data and self.cleaned_data['dns'])):
            for k in ['dns', 'ip']:
                if k not in self._errors:
                    self._errors[k] = ErrorList()
                self._errors[k].append('A machine must have an IP and/or DNS name.')
        # If DNS and IP already on DB, check that don't collide with other existing
        # Different machines must have different IPs/DNS
        # An IP can be shared by multiple machines if they have different DNS
        # A DNS can be shared by multiple machines if they have different IPs
        exists = Machine.exists(
            self.cleaned_data['ip'] if 'ip' in self.cleaned_data else None,
            self.cleaned_data['dns'] if 'dns' in self.cleaned_data else None
        )
        if exists:
            # Check that id is not of the machine (on edition)
            if 'id' not in self.cleaned_data or not self.cleaned_data['id'] or self.cleaned_data['id'] not in exists.values_list('id', flat=True):
                for k in ['dns', 'ip']:
                    if k in self.cleaned_data and self.cleaned_data[k]:
                        if k not in self._errors:
                            self._errors[k] = ErrorList()
                        self._errors[k].append(
                            "There is already a machine with this DNS/IP combination. You can't have two machines with the same!"
                        )
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


class MachineNameForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=True,
        validators=[validate_ip_or_dns],
        widget=forms.TextInput(attrs={'placeholder': 'Write the machine DNS or IP address', 'class': 'form-control'}),
        label="Machines names"
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if not validate_ip_or_dns(name):
            raise ValidationError('This is not a valid DNS nor IP address.')
        return name

    def clean(self):
        cleaned_data = super(MachineNameForm, self).clean()
        if 'name' not in cleaned_data: return cleaned_data
        # Check if DNS or IP and register attribute
        if validate_ip(cleaned_data['name']):
            cleaned_data['ip'] = cleaned_data['name']
        elif validate_dns(cleaned_data['name']):
            cleaned_data['dns'] = cleaned_data['name']
        # If DNS and IP already on DB, associate id
        cleaned_data['machine'] = None
        if 'dns' in cleaned_data and Machine.objects.filter(dns=cleaned_data['dns']).exists():
            cleaned_data['machine'] = Machine.objects.filter(dns=cleaned_data['dns']).first()
        elif 'ip' in cleaned_data and Machine.objects.filter(ip=cleaned_data['ip']).exists():
            cleaned_data['machine'] = Machine.objects.filter(ip=cleaned_data['ip']).first()
        return cleaned_data


class IPRangeForm(forms.Form):
    ip = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Base IP"
    )
    range = forms.ChoiceField(
        choices=[(n, n) for n in range(13, 33)][::-1],
        required=True,
        label="Range",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        if not validate_ip(ip):
            raise ValidationError('IP address is not valid.')
        return ip

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'ip' in cleaned_data:
            try:
                ipaddress.ip_network(f"{self.cleaned_data['ip']}/{self.cleaned_data['range']}")
            except ValueError:
                raise ValidationError("The IP given has the host bits set.", params={'range': cleaned_data['range']})
        return cleaned_data

    def validate_custom(self, worker):
        # Validate with default validator
        if not super(IPRangeForm, self).is_valid():
            return False
        # Start variables
        self.cleaned_data['machines'] = []
        self.cleaned_data['alreadyAssociated'] = 0
        self.cleaned_data['edit'] = False
        # Get ip addresses
        network = ipaddress.ip_network(f"{self.cleaned_data['ip']}/{self.cleaned_data['range']}")
        # For each entry
        for ip in network:
            # Create Machine objects
            mobj = Machine(
                ip=ip,
                dns=None
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
        self.cleaned_data['ignored'] = 0
        # Check if any machine is valid
        return len(self.cleaned_data['machines']) > 0




