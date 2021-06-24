from django.test import TestCase

from machines.forms import MachineWorkerBatchInputForm, MachineForm, MachineNameForm, IPRangeForm
from machines.models import Machine, MachineWorker
from workers.models import Worker


class MachineWorkerBatchInputFormTest(TestCase):

    def test_flag_edit(self):
        m = Machine.objects.create(id=1, dns='abc.pt')
        f = MachineWorkerBatchInputForm(data={'batch': 'abc.pt;def.pt'})
        # Edit
        self.assertTrue(f.validate_custom(None))
        self.assertEqual(f.cleaned_data['machines'][0].dns, m.dns)
        self.assertEqual(f.cleaned_data['machines'][0].id, m.id)
        self.assertTrue('edit' in f.cleaned_data['machines'][0].__dict__.keys())
        self.assertTrue(f.cleaned_data['machines'][0].edit)
        # Not edit
        self.assertEqual(f.cleaned_data['machines'][1].dns, 'def.pt')
        self.assertEqual(f.cleaned_data['machines'][1].id, None)
        self.assertFalse('edit' in f.cleaned_data['machines'][1].__dict__.keys())
        # Validate form global flag
        self.assertTrue(f.cleaned_data['edit'])

    def test_flag_alreadyAssociated(self):
        m = Machine.objects.create(id=1, dns='abc.pt')
        w = Worker.objects.create(name='STICUA')
        MachineWorker.objects.create(machine=m, worker=w)
        f = MachineWorkerBatchInputForm(data={'batch': 'abc.pt;def.pt'})
        # Associated
        self.assertTrue(f.validate_custom(w))
        self.assertEqual(f.cleaned_data['machines'][0].dns, m.dns)
        self.assertTrue('alreadyAssociated' in f.cleaned_data['machines'][0].__dict__.keys())
        self.assertTrue(f.cleaned_data['machines'][0].alreadyAssociated)
        # Not associated
        self.assertEqual(f.cleaned_data['machines'][1].dns, 'def.pt')
        self.assertFalse('alreadyAssociated' in f.cleaned_data['machines'][1].__dict__.keys())
        # Validate form global counter
        self.assertEqual(f.cleaned_data['alreadyAssociated'], 1)

    def test_invalid_ip_ignored(self):
        f = MachineWorkerBatchInputForm(data={'batch': '192.168.168.168;192.a.8.9'})
        self.assertTrue(f.validate_custom(None))
        self.assertEqual(len(f.cleaned_data['machines']), 1)
        self.assertEqual(f.cleaned_data['machines'][0].ip, '192.168.168.168')

    def test_invalid_dns_ignored(self):
        f = MachineWorkerBatchInputForm(data={'batch': 'abc.ajsya:a7/;def.pt'})
        self.assertTrue(f.validate_custom(None))
        self.assertEqual(len(f.cleaned_data['machines']), 1)
        self.assertEqual(f.cleaned_data['machines'][0].dns, 'def.pt')

    def test_allInvalid_returnInvalid(self):
        f = MachineWorkerBatchInputForm(data={'batch': 'abc.ajsya:a7/;192.a.8.9'})
        self.assertFalse(f.validate_custom(None))

    def test_valid_form(self):
        f = MachineWorkerBatchInputForm(data={'batch': '192.168.168.168;abc.pt'})
        self.assertTrue(f.validate_custom(None))
        self.assertEqual(len(f.cleaned_data['machines']), 2)
        self.assertEqual(f.cleaned_data['machines'][0].ip, '192.168.168.168')
        self.assertEqual(f.cleaned_data['machines'][0].dns, None)
        self.assertEqual(f.cleaned_data['machines'][1].ip, None)
        self.assertEqual(f.cleaned_data['machines'][1].dns, 'abc.pt')

    def test_all_splitters(self):
        f = MachineWorkerBatchInputForm(data={'batch': '192.168.168.168;abc.pt,def.pt\n  192.168.168.168'})
        self.assertTrue(f.validate_custom(None))
        self.assertEqual(len(f.cleaned_data['machines']), 4)
        self.assertEqual(f.cleaned_data['machines'][0].ip, '192.168.168.168')
        self.assertEqual(f.cleaned_data['machines'][1].dns, 'abc.pt')
        self.assertEqual(f.cleaned_data['machines'][2].dns, 'def.pt')
        self.assertEqual(f.cleaned_data['machines'][3].ip, '192.168.168.168')


class MachineFormTest(TestCase):

    def test_invalid_ip(self):
        f = MachineForm(data={'ip': '192.a.168.168'})
        self.assertFalse(f.is_valid())
        self.assertTrue('ip' in f.errors.keys(), msg='ip field expected in form errors')

    def test_invalid_dns(self):
        f = MachineForm(data={'dns': 'jasg/6&-'})
        self.assertFalse(f.is_valid())
        self.assertTrue('dns' in f.errors.keys(), msg='dns field expected in form errors')

    def test_not_ip_nor_dns(self):
        f = MachineForm(data={})
        self.assertFalse(f.is_valid())
        self.assertTrue('dns' in f.errors.keys(), msg='dns field expected in form errors')
        self.assertTrue('ip' in f.errors.keys(), msg='ip field expected in form errors')
        self.assertEqual(f.errors['dns'], ['A machine must have an IP and/or DNS name.'])
        self.assertEqual(f.errors['ip'], ['A machine must have an IP and/or DNS name.'])

    def test_duplicate_dns(self):
        Machine.objects.create(dns='abc.pt')
        f = MachineForm(data={'dns': 'abc.pt'})
        self.assertFalse(f.is_valid())
        self.assertTrue('dns' in f.errors.keys(), msg='dns field expected in form errors')
        self.assertEqual(f.errors['dns'], ['There is already a machine with this DNS/IP combination. You can\'t have two machines with the same!'])

    def test_duplicate_ip(self):
        Machine.objects.create(ip='192.168.168.168')
        f = MachineForm(data={'ip': '192.168.168.168'})
        self.assertFalse(f.is_valid())
        self.assertTrue('ip' in f.errors.keys(), msg='ip field expected in form errors')
        self.assertEqual(f.errors['ip'], ['There is already a machine with this DNS/IP combination. You can\'t have two machines with the same!'])

    def test_duplicate_dns_ip(self):
        Machine.objects.create(dns='abc.pt', ip='192.168.168.168')
        f = MachineForm(data={'dns': 'abc.pt', 'ip': '192.168.168.168'})
        self.assertFalse(f.is_valid())
        self.assertTrue('ip' in f.errors.keys(), msg='ip field expected in form errors')
        self.assertEqual(f.errors['ip'], ['There is already a machine with this DNS/IP combination. You can\'t have two machines with the same!'])
        self.assertTrue('dns' in f.errors.keys(), msg='ip field expected in form errors')
        self.assertEqual(f.errors['dns'], ['There is already a machine with this DNS/IP combination. You can\'t have two machines with the same!'])

    def test_duplicate_edit(self):
        Machine.objects.create(id=3, dns='abc.pt', ip='192.168.168.168')
        f = MachineForm(data={'id': 3, 'dns': 'abc.pt', 'ip': '192.168.168.168'})
        self.assertTrue(f.is_valid())
        self.assertTrue('id' in f.cleaned_data)
        self.assertEqual(f.cleaned_data['id'], 3)

    def test_valid_form(self):
        f = MachineForm(data={'dns': 'abc.pt', 'ip': '192.168.168.168'})
        self.assertTrue(f.is_valid())


class MachineNameFormTest(TestCase):

    def test_invalid_ip(self):
        f = MachineNameForm(data={'name': '192.a.2.3'})
        self.assertFalse(f.is_valid())

    def test_invalid_dns(self):
        f = MachineNameForm(data={'name': 'ajsgadga./&-'})
        self.assertFalse(f.is_valid())

    def test_valid_ip(self):
        f = MachineNameForm(data={'name': '192.168.168.168'})
        self.assertTrue(f.is_valid())

    def test_valid_dns(self):
        f = MachineNameForm(data={'name': 'abc.pt'})
        self.assertTrue(f.is_valid())

    def test_valid_exists_on_db(self):
        m = Machine.objects.create(dns='abc.pt')
        f = MachineNameForm(data={'name': 'abc.pt'})
        self.assertTrue(f.is_valid())
        self.assertTrue('machine' in f.cleaned_data)
        self.assertEqual(f.cleaned_data['machine'], m)


class IPRangeFormTest(TestCase):

    def test_invalid_ip(self):
        f = IPRangeForm(data={'ip': '192.a.168.168'})
        self.assertFalse(f.validate_custom(None))
        self.assertTrue('ip' in f.errors.keys())
        self.assertEqual(f.errors['ip'], ['IP address is not valid.'])

    def test_host_bits_set(self):
        f = IPRangeForm(data={'ip': '192.168.168.168', 'range': '24'})
        self.assertFalse(f.validate_custom(None))
        self.assertTrue('__all__' in f.errors.keys())
        self.assertEqual(f.errors['__all__'], ['The IP given has the host bits set.'])

    def test_flag_edit(self):
        Machine.objects.create(ip='192.192.192.254')
        f = IPRangeForm(data={'ip': '192.192.192.254', 'range': '31'})
        self.assertTrue(f.validate_custom(None))
        self.assertEqual(len(f.cleaned_data['machines']), 2)
        # Edit
        self.assertEqual(format(f.cleaned_data['machines'][0].ip), '192.192.192.254')
        self.assertTrue('edit' in f.cleaned_data['machines'][0].__dict__.keys())
        self.assertTrue(f.cleaned_data['machines'][0].edit)
        # Not edit
        self.assertEqual(format(f.cleaned_data['machines'][1].ip), '192.192.192.255')
        self.assertFalse('edit' in f.cleaned_data['machines'][1].__dict__.keys())
        # Form global var
        self.assertTrue(f.cleaned_data['edit'])

    def test_flag_associated(self):
        m = Machine.objects.create(ip='192.192.192.254')
        w = Worker.objects.create(name='STICUA')
        MachineWorker.objects.create(machine=m, worker=w)
        f = IPRangeForm(data={'ip': '192.192.192.254', 'range': '31'})
        self.assertTrue(f.validate_custom(w))
        self.assertEqual(len(f.cleaned_data['machines']), 2)
        # Edit
        self.assertEqual(format(f.cleaned_data['machines'][0].ip), '192.192.192.254')
        self.assertTrue('alreadyAssociated' in f.cleaned_data['machines'][0].__dict__.keys())
        self.assertTrue(f.cleaned_data['machines'][0].alreadyAssociated)
        # Not edit
        self.assertEqual(format(f.cleaned_data['machines'][1].ip), '192.192.192.255')
        self.assertFalse('alreadyAssociated' in f.cleaned_data['machines'][1].__dict__.keys())
        # Form global var
        self.assertEqual(f.cleaned_data['alreadyAssociated'], 1)

    def test_valid(self):
        f = IPRangeForm(data={'ip': '192.80.21.0', 'range': '24'})
        self.assertTrue(f.validate_custom(None))
        self.assertEqual(len(f.cleaned_data['machines']), 256)
