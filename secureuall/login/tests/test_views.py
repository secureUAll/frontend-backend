from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from login.models import User, UserAccessRequest
from machines.models import MachineUser, Machine


class LoginViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')


class WelcomeViewTest(TestCase):
    userpass = 'abc'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="new@test.pt", email="new@test.pt",
            password=WelcomeViewTest.userpass
        )
        User.objects.create_user(
            username="admin@test.pt", email="admin@test.pt",
            password=WelcomeViewTest.userpass,
            is_admin=True
        )
        u = User.objects.create_user(
            username="authorized@test.pt", email="authorized@test.pt",
            password=WelcomeViewTest.userpass,
            is_admin=True
        )
        MachineUser.objects.create(
            user=u,
            machine=Machine.objects.create(dns='abc.pt'),
            userType='S'
        )

    # View properties
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='new@test.pt', password=WelcomeViewTest.userpass)
        response = self.client.get('/welcome/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='new@test.pt', password=WelcomeViewTest.userpass)
        response = self.client.get(reverse('login:welcome'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='new@test.pt', password=WelcomeViewTest.userpass)
        response = self.client.get(reverse('login:welcome'))
        self.assertTemplateUsed(response, 'login/welcome.html')

    # User logged
    def test_logged_new_user_rendered(self):
        self.client.login(username='new@test.pt', password=WelcomeViewTest.userpass)
        response = self.client.get(reverse('login:welcome'))
        # Check view properties
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/welcome.html')
        # Validate context
        self.assertFalse(response.context['requests']['pending'].exists(), msg='New user has pending requests!')
        self.assertFalse(response.context['requestSubmitted'], msg='New user has request submitted without submitting!')

    # Redirect
    def test_not_logged_redirected_to_login(self):
        response = self.client.get('/welcome/')
        self.assertRedirects(
            response=response,
            expected_url='/login/?next=/welcome/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )

    def test_logged_admin_redirected_to_home(self):
        self.client.login(username='admin@test.pt', password=WelcomeViewTest.userpass)
        response = self.client.get('/welcome/')
        self.assertRedirects(
            response=response,
            expected_url='/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )

    def test_logged_authorized_redirected_to_home(self):
        self.client.login(username='authorized@test.pt', password=WelcomeViewTest.userpass)
        response = self.client.get('/welcome/')
        self.assertRedirects(
            response=response,
            expected_url='/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False
        )


class ProfileViewTest(TestCase):
    userpass="abc"

    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(
            username="authorized@test.pt", email="authorized@test.pt",
            password=ProfileViewTest.userpass,
            is_admin=True
        )
        MachineUser.objects.create(
            user=u,
            machine=Machine.objects.create(dns='abc.pt'),
            userType='S'
        )

    # View properties
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='authorized@test.pt', password=ProfileViewTest.userpass)
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='authorized@test.pt', password=ProfileViewTest.userpass)
        response = self.client.get(reverse('login:profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='authorized@test.pt', password=ProfileViewTest.userpass)
        response = self.client.get(reverse('login:profile'))
        self.assertTemplateUsed(response, 'login/profile.html')


class AboutViewTest(TestCase):

    # View properties
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login:about'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login:about'))
        self.assertTemplateUsed(response, 'login/about.html')

