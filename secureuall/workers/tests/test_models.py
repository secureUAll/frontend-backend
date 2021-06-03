from django.test import TestCase

from login.models import User
from machines.models import Scan, Machine
from workers.models import Worker, WorkerScanComment


class WorkerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Worker.objects.create(
            id=1,
            name="Worker ABC"
        )

    def test_str(self):
        w = Worker.objects.get(id=1)
        self.assertEqual(str(w), w.name)


class WorkerScanCommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        s = Scan.objects.create(
            id=1,
            machine=Machine.objects.create(dns='abc.pt'),
            worker=Worker.objects.create(name="Worker ABC"),
            status='Done'
        )
        WorkerScanComment.objects.create(
            id=1,
            scan=s,
            comment='Loren ipsum...',
            user_cod=User.objects.create(username="admin@test.pt")
        )

    def test_str(self):
        wsc = WorkerScanComment.objects.get(id=1)
        self.assertEqual(str(wsc), wsc.comment)
