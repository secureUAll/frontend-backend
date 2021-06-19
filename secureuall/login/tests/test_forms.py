from django.test import TestCase

# Create your tests here.
from login.forms import UserAccessRequestApprovalForm
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

