from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from .views import DeleteUserView, SignUpView, SendNewsletterView
from .models import UserInfo
from .forms import NewsletterForm, DeleteForm


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


class TestModels(TestCase):

    def setUp(self) -> None:
        self.user1 = UserInfo.objects.create(
            email='test@test.com',
            name='Test',
            localization='Test123'
        )

    def test_str_email(self):
        self.assertEqual(self.user1.email, 'test@test.com')


class TestForms(SimpleTestCase):

    def test_delete_form_valid_data(self):
        form = DeleteForm(data={
             'email': 'test@test.com'
        })

        self.assertTrue(form.is_valid())

    def test_delete_form_no_data(self):
        form = DeleteForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_newsletter_form_valid_data(self):
        form = NewsletterForm(data={
            'subject': 'This is a test subject of a newsletter',
            'receivers': 'test@test.com',
            'message': 'This is a simple text'
        })

        self.assertTrue(form.is_valid())

    def test_newsletter_form_no_data(self):
        form = NewsletterForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)