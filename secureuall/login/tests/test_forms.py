from django.test import TestCase

# Create your tests here.
from login.forms import UserAccessRequestApprovalForm, RequestAccessForm, UserNotificationForm
from login.models import UserAccessRequest, User


class UserAccessRequestApprovalFormTest(TestCase):

    def test_clean_request_test_valid_request(self):
        UserAccessRequest.objects.create(id=99, user=User.objects.create(username="user@use.pt"))
        f = UserAccessRequestApprovalForm(data={'request': 99})
        self.assertTrue(f.is_valid())

    def test_clean_request_test_invalid_request(self):
        f = UserAccessRequestApprovalForm(data={'request': 3})
        self.assertFalse(f.is_valid())
        self.assertTrue('request' in f.errors.keys(), msg='request field expected in form errors')
        self.assertEqual(f.errors['request'], ["Request is not valid!"])


class RequestAccessFormTest(TestCase):

    def test_email_readonly(self):
        f = RequestAccessForm()
        self.assertEquals(f.fields['email'].widget.attrs['readonly'], 'readonly')


class UserNotificationFormTest(TestCase):

    def test_invalid_type(self):
        f = UserNotificationForm(data={'type': 'Wrong type', 'active': False, 'value': 'abc'})
        self.assertFalse(f.is_valid())
        self.assertTrue('type' in f.errors.keys(), msg='type field expected in form errors')
        self.assertEqual(f.errors['type'], ['Notification type is not valid!'])

    def test_invalid_valueMissing(self):
        f = UserNotificationForm(data={'type': 'Microsoft Teams', 'active': True, 'value': ''})
        self.assertFalse(f.is_valid())
        self.assertTrue('__all__' in f.errors.keys(), msg='value field expected in form errors')
        self.assertEqual(f.errors['__all__'], ['The value is mandatory for active notifications!'])

    def test_MicrosoftTeamsRegex(self):
        f = UserNotificationForm(data={'type': 'Microsoft Teams', 'active': True, 'value': 'https://google.com'})
        self.assertFalse(f.is_valid())
        self.assertTrue('__all__' in f.errors.keys(), msg='value field expected in form errors')
        self.assertEqual(f.errors['__all__'], ['Value is not valid for selected type.'])

    def test_valid_email(self):
        f = UserNotificationForm(data={'type': 'Email', 'active': True, 'value': 'email@ua.pt'})
        self.assertTrue(f.is_valid())

    def test_valid_MicrosoftTeams(self):
        f = UserNotificationForm(data={'type': 'Microsoft Teams', 'active': True, 'value': 'https://webhook.office.com/abc'})
        self.assertTrue(f.is_valid())



