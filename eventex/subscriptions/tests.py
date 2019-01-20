from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/subscription/')

    def test_get(self):
        """GET /subscription/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """Html must contain CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))
