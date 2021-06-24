from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from machines.models import Machine, MachineUser, Scan, MachineService, MachinePort, Vulnerability, VulnerabilityComment
from login.models import User
from workers.models import Worker


class MachineModelTest(TestCase):

    def test_str(self):
        m1 = Machine.objects.create(dns="ua.pt", ip="192.168.168.168")
        self.assertEqual(str(m1), "192.168.168.168 / ua.pt")
        m2 = Machine.objects.create(dns="ua.pt")
        self.assertEqual(str(m2), "ua.pt")
        m3 = Machine.objects.create(ip="192.168.168.168")
        self.assertEqual(str(m3), "192.168.168.168")

    def test_constraint_ip_and_or_dns(self):
        with self.assertRaises(IntegrityError):
            Machine.objects.create(dns=None, ip=None)

    def test_is_ip_pos(self):
        self.assertTrue(Machine.is_ip('192.168.152.156'))

    def test_is_ip_neg(self):
        self.assertFalse(Machine.is_ip('192.a.152.156'))

    def test_is_dns_pos(self):
        self.assertTrue(Machine.is_dns('abc.pt'))

    def test_is_dns_neg(self):
        self.assertFalse(Machine.is_dns('absg%&2ngs-'))

    def test_exists(self):
        # Different machines must have different IPs/DNS
        # An IP can be shared by multiple machines if they have different DNS
        # A DNS can be shared by multiple machines if they have different IPs
        m = Machine.objects.create(dns="ua.pt", ip="192.168.168.168")
        self.assertTrue(Machine.exists(dns=m.dns, ip=m.ip).exists())
        self.assertFalse(Machine.exists(dns=m.dns, ip=None).exists())
        self.assertFalse(Machine.exists(dns=None, ip=m.ip).exists())
        m = Machine.objects.create(dns="stic.pt")
        self.assertFalse(Machine.exists(dns=m.dns, ip='192.167.167.167').exists())
        self.assertTrue(Machine.exists(dns=m.dns, ip=None).exists())
        m = Machine.objects.create(ip="192.167.167.167")
        self.assertFalse(Machine.exists(dns='dns.pt', ip=m.ip).exists())
        self.assertTrue(Machine.exists(dns=None, ip=m.ip).exists())


class MachineUserModelTest(TestCase):

    def test_unique_constraint(self):
        m = Machine.objects.create(dns="ua.pt", ip="192.168.168.168")
        u = User.objects.create(username="normalhascess@test.pt", is_admin=False)
        with self.assertRaises(IntegrityError):
            MachineUser.objects.create(user=u, machine=m)
            MachineUser.objects.create(user=u, machine=m)


class ScanModelTest(TestCase):

    def test_str(self):
        # Example output: 2021-06-24 21:12:00.800139+00:00 at STIC
        m = Machine.objects.create(dns="ua.pt", ip="192.168.168.168")
        w = Worker.objects.create(name="STIC")
        s = Scan.objects.create(machine=m, worker=w)
        now = str(timezone.now())
        string = str(s)
        self.assertEqual(string.split("+")[0].split(".")[0], now.split(".")[0])
        self.assertEqual(string.split("+")[1], now.split("+")[1] + " at STIC")


class MachineServiceModelTest(TestCase):

    def test_str(self):
        ms = MachineService.objects.create(service='nginx', version='1.2.4.2')
        self.assertEqual(str(ms), f"{ms.service} ({ms.version})")

    def test_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            MachineService.objects.create(service='nginx', version='1.2.4.2')
            MachineService.objects.create(service='nginx', version='1.2.4.2')


class MachinePortModelTest(TestCase):

    def test_str(self):
        m = Machine.objects.create(dns="ua.pt", ip="192.168.168.168")
        ms = MachineService.objects.create(service='nginx', version='1.2.4.2')
        mp = MachinePort.objects.create(machine=m, port=123, service=ms)
        self.assertEqual(str(mp), f"{mp.service} ({mp.port})")

    def test_unique_constraint(self):
        m = Machine.objects.create(dns="ua.pt", ip="192.168.168.168")
        ms = MachineService.objects.create(service='nginx', version='1.2.4.2')
        with self.assertRaises(IntegrityError):
            MachinePort.objects.create(machine=m, port=123, service=ms, scanEnabled=True)
            MachinePort.objects.create(machine=m, port=123, service=ms, scanEnabled=True)


class VulnerabilityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        m = Machine.objects.create(dns="ua.pt", ip="192.168.168.168")
        w = Worker.objects.create(name="STIC")
        s = Scan.objects.create(machine=m, worker=w)
        Vulnerability.objects.create(
            id=25,
            risk=1,
            type='SQL Injection',
            description='Loren ipsum',
            location='https://paco.ua.pt https://ua.pt https://publico.pt',
            status='FIXED',
            machine=m,
            scan=s
        )

    def test_str(self):
        v = Vulnerability.objects.get(id=25)
        self.assertEqual(str(v), f"({v.risk}) {v.description}")

    def test_location_split(self):
        v = Vulnerability.objects.get(id=25)
        self.assertEqual(v.locationsplit(), ['https://paco.ua.pt', 'https://ua.pt', 'https://publico.pt'])

    def test_getriskdisplay(self):
        v = Vulnerability.objects.get(id=25)
        self.assertEqual(v.getriskdisplay(), 1)
        v.risk = 0
        self.assertEqual(v.getriskdisplay(), "unclassified")


class VulnerabilityCommentModelTest(TestCase):

    def test_str(self):
        m = Machine.objects.create(dns="ua.pt", ip="192.168.168.168")
        u = User.objects.create(username="normalhascess@test.pt", is_admin=False)
        w = Worker.objects.create(name="STIC")
        s = Scan.objects.create(machine=m, worker=w)
        v = Vulnerability.objects.create(
            id=25,
            risk=1,
            type='SQL Injection',
            description='Loren ipsum',
            location='https://paco.ua.pt https://ua.pt https://publico.pt',
            status='FIXED',
            machine=m,
            scan=s
        )
        vc = VulnerabilityComment.objects.create(
            vulnerability=v,
            user=u,
            comment='Loren ipsummmm'
        )
        self.assertEqual(str(vc), vc.comment)

