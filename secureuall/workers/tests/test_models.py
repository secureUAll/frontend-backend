from django.test import TestCase

from workers.models import Worker, WorkerScanComment
from machines.models import Scan, Machine
from login.models import User


class WorkerModelTest(TestCase):

    def test_str(self):
        w = Worker.objects.create(name='STICUA')
        self.assertEqual(str(w), w.name)


class WorkerScanCommentModelTest(TestCase):

    def test_str(self):
        u = User.objects.create(username="normalhascess@test.pt", is_admin=False)
        m = Machine.objects.create(dns="ua.pt", ip="192.168.168.168")
        w = Worker.objects.create(name="STIC")
        s = Scan.objects.create(machine=m, worker=w)
        wsc = WorkerScanComment.objects.create(comment='LOREN IPSUMMM', scan=s, user_cod=u)
        self.assertEqual(str(wsc), wsc.comment)
