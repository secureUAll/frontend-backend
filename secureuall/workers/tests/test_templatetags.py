from django.test import SimpleTestCase

from ..templatetags.workers_filters import *


class WorkerTemplateTagsTests(SimpleTestCase):

    def test_color(self):
        self.assertEqual(color('active'), 'primary')
        self.assertEqual(color('down'), 'danger')
        self.assertEqual(color('abc'), 'dark')
