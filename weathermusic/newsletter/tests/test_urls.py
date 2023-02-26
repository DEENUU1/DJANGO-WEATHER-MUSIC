from django.test import SimpleTestCase
from django.urls import resolve, reverse

from newsletter.views import DeleteUserView, SignUpView, SendNewsletterView


class TestUrls(SimpleTestCase):
    """ Test Cases for Urls in Django """
    def test_register_url_resolve(self):
        """ Test for the sign up view """
        url = reverse('newsletter:register')
        self.assertEqual(resolve(url).func.view_class, SignUpView)

    def test_delete_url_resolve(self):
        """ Test for the delete user view """
        url = reverse('newsletter:delete')
        self.assertEqual(resolve(url).func.view_class, DeleteUserView)

    def test_send_newsletter_url_resolve(self):
        """ Test for send newsletter view """
        url = reverse('newsletter:send')
        self.assertEqual(resolve(url).func.view_class, SendNewsletterView)
