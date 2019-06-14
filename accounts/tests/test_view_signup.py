from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

from ..forms import SignUpForm
from ..views import signup


class SignUpTests(TestCase):
    def setUp(self):
        self.response = self.client.get('/signup/')

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_view_resolves(self):
        view = resolve('/signup/')
        self.assertEqual(view.func, signup)

    def test_signup_csrf_present(self):
        self.assertContains(self.response, '"csrfmiddlewaretoken"')

    def test_signup_form_instance(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'N0tAPa$$word',
            'password2': 'N0tAPa$$word'
        }
        self.response = self.client.post('/signup/', data)

    def test_redirection(self):
        self.assertRedirects(self.response, '/')

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get('/')
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, 'john')


class InvalidSignUpTests(TestCase):
    def setUp(self):
        data = {}
        self.response = self.client.post('/signup/', data)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_user_not_created(self):
        self.assertFalse(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get('/')
        user = response.context.get('user')
        self.assertFalse(user.is_authenticated)
