from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.
from login.models import User, UserAccessRequest
from machines.models import MachineUser, Machine


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name="Manuel", last_name="Pereira", username="admin@test.pt", is_admin=True)
        u = User.objects.create(username="normalhascess@test.pt", is_admin=False)
        m = Machine.objects.create(dns="ua.pt")
        MachineUser.objects.create(user=u, machine=m, userType='S')
        User.objects.create(username="normalwithoutacess@test.pt", is_admin=False)

    def test_has_access_method_positive(self):
        self.assertTrue(User.has_access(User.objects.get(username="admin@test.pt")))
        self.assertTrue(User.has_access(User.objects.get(username="normalhascess@test.pt")))

    def test_has_access_method_negative(self):
        self.assertFalse(User.has_access(User.objects.get(username="normalwithoutacess@test.pt")))

    def test_str(self):
        u = User.objects.get(username="admin@test.pt")
        self.assertEqual(str(u), u.get_full_name())


class UserAccessRequestModelTest(TestCase):
    machines = ['abc.pt ', '125.236.256.236', 'deg.pt']

    @classmethod
    def setUpTestData(cls):
        u = User.objects.create(username="normalwithoutacess@test.pt", is_admin=False)
        UserAccessRequest.objects.create(
            id=1, user=u, role='S', motive='Loren ipsum', notes='Loren ipsum',
            machines=';'.join(UserAccessRequestModelTest.machines),
            approved=False,
            pending=True
        )
        UserAccessRequest.objects.create(
            id=2, user=u, role='S', motive='Loren ipsum', notes='Loren ipsum',
            machines=';'.join(UserAccessRequestModelTest.machines),
            approved=True,
            pending=False
        )
        UserAccessRequest.objects.create(
            id=3, user=u, role='S', motive='Loren ipsum', notes='Loren ipsum',
            machines=';'.join(UserAccessRequestModelTest.machines),
            approved=False,
            pending=False
        )

    def test_get_machines(self):
        self.assertEqual(
            UserAccessRequest.objects.get(id=1).get_machines(),
            [m.strip() for m in UserAccessRequestModelTest.machines]
        )

    def test_get_status_pending(self):
        self.assertEqual(
            UserAccessRequest.objects.get(id=1).get_status(),
            "Pending approval"
        )

    def test_get_status_approved(self):
        self.assertEqual(
            UserAccessRequest.objects.get(id=2).get_status(),
            "Approved"
        )

    def test_get_status_denied(self):
        self.assertEqual(
            UserAccessRequest.objects.get(id=3).get_status(),
            "Denied"
        )

    def test_constraint_if_approved_not_pending(self):
        u = User.objects.get(username="normalwithoutacess@test.pt")
        with self.assertRaises(IntegrityError):
            UserAccessRequest.objects.create(
                id=4, user=u, role='S', motive='Loren ipsum', notes='Loren ipsum',
                machines=';'.join(UserAccessRequestModelTest.machines),
                approved=True,
                pending=True
            )
