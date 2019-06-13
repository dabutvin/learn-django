from django.urls import resolve
from django.test import TestCase

from .models import Board
from .views import home, board_topics


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


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
