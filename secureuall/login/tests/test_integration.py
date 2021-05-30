from os import wait

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from login.models import User


class WelcomeIntegrationTest(StaticLiveServerTestCase):
    userpass = 'abc'

    @classmethod
    def setUpClass(cls):
        # Populate database
        User.objects.create_user(username="new@test.pt", email="new@test.pt")
        # Selenium start up
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_new_user_request_access(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        # Log user in
        email_field = self.selenium.find_element_by_id('loginEmailAddres')
        email_field.send_keys('new@test.pt')
        self.selenium.find_element_by_css_selector('form button.btn').click()
        # Validate title
        title = self.selenium.find_element_by_css_selector('h4.card-title')
        self.assertEqual(title.text, 'Request access to machines vulnerabilities data')
        # Validate page has alert
        alert = self.selenium.find_element_by_css_selector('div.border-warning p.text-warning')
        self.assertTrue(
            'You don\'t have access to the dashboard!' in alert.text,
            msg='Alert title does not match expected!'
        )
        # Validate form has email filled already and is blocked
        form_email = self.selenium.find_element_by_css_selector('form input#id_email')
        self.assertEqual(form_email.get_attribute('value'), 'new@test.pt')
        self.assertTrue(form_email.get_attribute('readonly'))
        # TODO Request acess to machine and validate that it was made