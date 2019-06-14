from django.contrib.auth.models import User
from django.urls import resolve
from django.test import TestCase

from .forms import NewTopicForm
from .models import Board, Topic, Post
from .views import home, board_topics, new_topic


class HomeTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        self.response = self.client.get('/')

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics(self):
        self.assertContains(self.response, 'href="/boards/1/"')


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        response = self.client.get('/boards/1/')
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_notfound_status_code(self):
        response = self.client.get('/boards/12124/')
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contains_navigation(self):
        response = self.client.get('/boards/1/')
        self.assertContains(response, 'href="/"')
        self.assertContains(response, 'href="/boards/1/new"')


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create(
            username='john', email='john@doe.com', password='123')

    def test_new_topic_view_success_status_code(self):
        response = self.client.get('/boards/1/new/')
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_notfound_status_code(self):
        response = self.client.get('/boards/123/new/')
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_to_board(self):
        response = self.client.get('/boards/1/new/')
        self.assertContains(response, 'href="/boards/1/"')

    def test_new_topic_view_contains_form(self):
        response = self.client.get('/boards/1/new/')
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_csrf_present(self):
        response = self.client.get('/boards/1/new/')
        self.assertContains(response, '"csrfmiddlewaretoken"')

    def test_post_valid_data(self):
        data = {
            'subject': 'New subject',
            'message': 'New message'
        }
        response = self.client.post('/boards/1/new/', data=data)

        self.assertEquals(response.status_code, 302)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_post_invalid_data(self):
        data = {}
        response = self.client.post('/boards/1/new/', data=data)
        form = response.context.get('form')

        # TODO: will the data exist across tests?
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_post_invalid_missing_data(self):
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post('/boards/1/new/', data=data)

        # TODO: will the data exist across tests?
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

        self.assertEquals(response.status_code, 200)
