from django.core import mail
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


class SubscriptionPostTest(TestCase):
    def setUp(self):
        data = dict(name='Dilan Nery', cpf='12345678901',
                    email='dilan@nery.net', phone='55-55555-5555')
        self.resp = self.client.post('/subscription/', data)

    def test_post(self):
        """Valid POST should redirect to /subscription/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        """Email subject must be 'Confirmação de Inscrição'"""
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        """Email must be from contato@eventex.com"""
        email = mail.outbox[0]
        expect = 'contato@eventex.com'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        """Email must be sent to the user and to the sender"""
        email = mail.outbox[0]
        expect = ['contato@eventex.com', 'dilan@nery.net']
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        """Email body must contain name, cpf, email and phone"""
        email = mail.outbox[0]
        for content in ('Dilan Nery', '12345678901', 'dilan@nery.net', '55-55555-5555'):
            self.assertIn(content, email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/subscription/', {})

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Dilan Nery', cpf='12345678901',
                    email='dilan@nery.net', phone='55-55555-5555')
        response = self.client.post('/subscription/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso')
