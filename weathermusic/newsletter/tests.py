from django.test import SimpleTestCase
from django.urls import resolve, reverse
from .views import DeleteUserView, SignUpView, SendNewsletterView


class TestUrls(SimpleTestCase):

    def test_register_url_resolve(self):
        url = reverse('newsletter:register')
        self.assertEqual(resolve(url).func.view_class, SignUpView)

    def test_delete_url_resolve(self):
        url = reverse('newsletter:delete')
        self.assertEqual(resolve(url).func.view_class, DeleteUserView)

    def test_send_newsletter_url_resolve(self):
        url = reverse('newsletter:send')
        self.assertEqual(resolve(url).func.view_class, SendNewsletterView)