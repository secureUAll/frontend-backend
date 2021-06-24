from django.test import TestCase
from django.urls import reverse

from machines.models import Machine, MachineUser, Log
from login.models import User
from workers.models import Worker


class MachinesViewTest(TestCase):
    userpass = "abc"

    @classmethod
    def setUp(cls):
        m = Machine.objects.create(id=3, dns='abc.pt')
        u = User.objects.create_user(
            username="authorized@test.pt", email="authorized@test.pt",
            password=MachinesViewTest.userpass,
            is_admin=True
        )
        MachineUser.objects.create(
            user=u,
            machine=m,
            userType='S'
        )

    # View properties
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='authorized@test.pt', password=MachinesViewTest.userpass)
        response = self.client.get('/machines/3')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='authorized@test.pt', password=MachinesViewTest.userpass)
        response = self.client.get(reverse('machines:machines', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='authorized@test.pt', password=MachinesViewTest.userpass)
        response = self.client.get(reverse('machines:machines', kwargs={'id': 3}))
        self.assertTemplateUsed(response, 'machines/machines.html')


class RequestsViewTest(TestCase):

    @classmethod
    def setUp(cls):
        m = Machine.objects.create(id=3, dns='abc.pt')
        u = User.objects.create_user(
            username="authorized@test.pt", email="authorized@test.pt",
            password=MachinesViewTest.userpass,
            is_admin=True
        )
        MachineUser.objects.create(
            user=u,
            machine=m,
            userType='S'
        )

    # View properties
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='authorized@test.pt', password=MachinesViewTest.userpass)
        response = self.client.get('/machines/requests')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='authorized@test.pt', password=MachinesViewTest.userpass)
        response = self.client.get(reverse('machines:requests'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='authorized@test.pt', password=MachinesViewTest.userpass)
        response = self.client.get(reverse('machines:requests'))
        self.assertTemplateUsed(response, 'machines/requests.html')


class LogViewTest(TestCase):
    userpass = 'abc'

    @classmethod
    def setUpTestData(cls):
        m=Machine.objects.create(id=3, dns='abc.pt')
        User.objects.create_user(
            username="admin@test.pt", email="admin@test.pt",
            password=LogViewTest.userpass,
            is_admin=True
        )
        Log.objects.create(
            cod=755,
            machine=m,
            worker=Worker.objects.create(id=1, name='STIC')
        )

    # View properties
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='admin@test.pt', password=LogViewTest.userpass)
        response = self.client.get('/machines/logs/755')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='admin@test.pt', password=LogViewTest.userpass)
        response = self.client.get(reverse('machines:getLog', kwargs={'id': 755}))
        self.assertEqual(response.status_code, 200)





