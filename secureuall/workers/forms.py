from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from machines.models import Machine
from .models import Worker

class MachineWorkerForm(forms.Form):
    machine = forms.CharField(
        max_length=300,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label="Host"
    )
    # Control variables
    id = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    # Create worker fields dynamically, based on db
    # Based on https://stackoverflow.com/questions/411761/variable-number-of-inputs-with-django-forms-possible
    def __init__(self, *args, **kwargs):
        super(MachineWorkerForm, self).__init__(*args, **kwargs)
        # Create fields for workers
        for w in Worker.objects.all():
            self.fields[f'worker_{w.id}'] = forms.BooleanField(label=w.name, required=False)

    def clean_id(self):
        id = self.cleaned_data['id']
        if not Machine.objects.filter(id=id).exists():
            raise ValidationError('Error validating machine.', params={'id', id})
        return id

    def clean(self):
        cleaned_data = super(MachineWorkerForm, self).clean()
        # Validate that worker fields are valid
        self.cleaned_data['workersTrue'] = set()
        self.cleaned_data['workersFalse'] = set()
        for k in cleaned_data.keys():
            if 'worker_' in k:
                wid = k.split('worker_')[1]
                if not Worker.objects.filter(id=wid).exists():
                    if k not in self._errors:
                        self._errors[k] = ErrorList()
                    self._errors[k].append(
                        "Invalid worker!"
                    )
                else:
                    if self.cleaned_data[k]:
                        self.cleaned_data['workersTrue'].add(int(wid))
                    else:
                        self.cleaned_data['workersFalse'].add(int(wid))
        self.cleaned_data['workersTrue'] = list(self.cleaned_data['workersTrue'])
        self.cleaned_data['workersFalse'] = list(self.cleaned_data['workersFalse'])
        return cleaned_data
