from django.test import TestCase
from django.urls import reverse

from login.models import User
from machines.models import Machine, MachineWorker
from workers.models import Worker


class WorkersViewTest(TestCase):
    userpass = 'abc'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="new@test.pt", email="new@test.pt",
            password=WorkersViewTest.userpass
        )
        User.objects.create_user(
            username="admin@test.pt", email="admin@test.pt",
            password=WorkersViewTest.userpass,
            is_admin=True
        )
        Worker.objects.create(id=1, name="Worker ABC")
        Worker.objects.create(id=2, name="Worker DEF")
        w = Worker.objects.create(id=3, name="Worker GHI")
        m = Machine.objects.create(id=1, dns="abc.pt")
        Machine.objects.create(id=2, dns="def.pt")
        MachineWorker.objects.create(
            id=1,
            worker=w, machine=m
        )

    # Tests for denied access (not logged and logged but not admin)
    def test_not_logged_redirected_to_login(self):
        response = self.client.get(reverse('workers:workers'))
        self.assertRedirects(
            response=response,
            expected_url=reverse('dashboard:dashboard'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )

    def test_logged_not_admin_redirected_to_login(self):
        self.client.login(username='new@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get(reverse('workers:workers'))
        self.assertRedirects(
            response=response,
            expected_url=reverse('dashboard:dashboard'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )

    # Tests for admin (that has access)
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='admin@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get('/workers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='admin@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get(reverse('workers:workers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='admin@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get(reverse('workers:workers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workers/workers.html')

    def test_context(self):
        self.client.login(username='admin@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get(reverse('workers:workers'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['workers'], Worker.objects.all().order_by('-created'))
        self.assertEqual(response.context['machinesWithoutWorker'], 1)
        self.assertFalse(response.context['machinesAdded'])


class AddMachinesViewTest(TestCase):
    userpass = 'abc'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="new@test.pt", email="new@test.pt",
            password=AddMachinesViewTest.userpass
        )
        User.objects.create_user(
            username="admin@test.pt", email="admin@test.pt",
            password=AddMachinesViewTest.userpass,
            is_admin=True
        )
        Worker.objects.create(id=1, name="Worker ABC")
        Worker.objects.create(id=2, name="Worker DEF")
        w = Worker.objects.create(id=3, name="Worker GHI")
        m = Machine.objects.create(id=1, dns="abc.pt")
        Machine.objects.create(id=2, dns="def.pt")
        MachineWorker.objects.create(
            id=1,
            worker=w, machine=m
        )

    # Tests for denied access (not logged and logged but not admin)
    def test_not_logged_redirected_to_login(self):
        response = self.client.get(reverse('workers:addMachines', kwargs={'id': 3}))
        self.assertRedirects(
            response=response,
            expected_url=reverse('dashboard:dashboard'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )
        response = self.client.get(reverse('workers:editMachines', kwargs={'id': 3}))
        self.assertRedirects(
            response=response,
            expected_url=reverse('dashboard:dashboard'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )

    def test_logged_not_admin_redirected_to_login(self):
        self.client.login(username='new@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get(reverse('workers:addMachines', kwargs={'id': 3}))
        self.assertRedirects(
            response=response,
            expected_url=reverse('dashboard:dashboard'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )
        response = self.client.get(reverse('workers:editMachines', kwargs={'id': 3}))
        self.assertRedirects(
            response=response,
            expected_url=reverse('dashboard:dashboard'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )

    # There is also a denied access when trying to edit machines on a worker without machine
    def test_logged_admin_edit_worker_without_machines(self):
        self.client.login(username='admin@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get(reverse('workers:editMachines', kwargs={'id': 1}))
        self.assertRedirects(
            response=response,
            expected_url=reverse('workers:workers'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )

    # Tests for admin (that has access)
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='admin@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get('/workers/3/machines/add')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/workers/3/machines/edit')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='admin@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get(reverse('workers:addMachines', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('workers:editMachines', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='admin@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get(reverse('workers:addMachines', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workers/addMachines.html')
        response = self.client.get(reverse('workers:editMachines', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workers/editMachines.html')

    def test_view_context(self):
        self.client.login(username='admin@test.pt', password=WorkersViewTest.userpass)
        response = self.client.get(reverse('workers:addMachines', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Add machines')
        self.assertEqual(response.context['worker'], Worker.objects.get(id=3))
        self.assertTrue(response.context['add'])
        self.assertEqual(response.context['ignored'], 0)
        response = self.client.get(reverse('workers:editMachines', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Edit machines list')
        self.assertEqual(response.context['worker'], Worker.objects.get(id=3))
        self.assertFalse(response.context['add'])
        self.assertEqual(response.context['ignored'], 0)
