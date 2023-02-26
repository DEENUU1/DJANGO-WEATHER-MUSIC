from django.test import SimpleTestCase

from newsletter.forms import NewsletterForm, DeleteForm


class TestForms(SimpleTestCase):
    """ Test Cases for forms in Django"""
    def test_delete_form_valid_data(self):
        """ Test for valid data"""
        form = DeleteForm(data={
             'email': 'test@test.com'})
        self.assertTrue(form.is_valid())

    def test_delete_form_no_data(self):
        """ Test for empty form """
        form = DeleteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_newsletter_form_valid_data(self):
        """ Test for newsletter valid data """
        form = NewsletterForm(data={
            'subject': 'This is a test subject of a newsletter',
            'receivers': 'test@test.com',
            'message': 'This is a simple text'})
        self.assertTrue(form.is_valid())

    def test_newsletter_form_no_data(self):
        """ Test for empty newsletter form data """
        form = NewsletterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)