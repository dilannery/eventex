from django.test import TestCase


class HomeTest(TestCase):
    def setUp(self):
        self.request = self.client.get('/')

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.request.status_code)

    def test_template(self):
        """GET / must use index.html"""
        self.assertTemplateUsed(self.request, 'index.html')
