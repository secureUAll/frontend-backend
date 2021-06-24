from django import forms
from django.test import TestCase

from workers.forms import MachineWorkerForm
from workers.models import Worker
from machines.models import Machine


class MachineWorkerFormTest(TestCase):

    def test_worker_fields_dynamically_generated(self):
        Worker.objects.create(id=1, name='STIC')
        Worker.objects.create(id=2, name='IEETA')
        Worker.objects.create(id=3, name='IT')
        f = MachineWorkerForm()
        self.assertTrue('worker_1' in f.fields)
        self.assertTrue('worker_2' in f.fields)
        self.assertTrue('worker_3' in f.fields)
        self.assertFalse('worker_4' in f.fields)

    def test_invalid_machine_id(self):
        f = MachineWorkerForm(data={'machine': 'abc.pt', 'id': 3})
        self.assertFalse(f.is_valid())
        self.assertTrue('id' in f.errors.keys())

    def test_invalid_worker_id(self):
        f = MachineWorkerForm(data={'machine': 'abc.pt', 'id': 3})
        f.fields['worker_10'] = forms.BooleanField(label='STIC', required=False)
        self.assertFalse(f.is_valid())
        self.assertTrue('worker_10' in f.errors.keys())

    def test_valid(self):
        Worker.objects.create(id=1, name='STIC')
        Worker.objects.create(id=2, name='IEETA')
        Machine.objects.create(id=3, dns='abc.pt')
        f = MachineWorkerForm(data={'machine': 'abc.pt', 'id': 3, 'worker_1': True, 'worker_2': False})
        self.assertTrue(f.is_valid())
        self.assertEqual(len(f.cleaned_data['workersTrue']), 1)
        self.assertEqual(f.cleaned_data['workersTrue'][0], 1)
        self.assertEqual(len(f.cleaned_data['workersFalse']), 1)
        self.assertEqual(f.cleaned_data['workersFalse'][0], 2)

