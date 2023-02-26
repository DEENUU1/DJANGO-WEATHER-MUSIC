from django.test import TestCase

from newsletter.models import UserInfo


class TestModels(TestCase):
    """ Test Cases for models in Django """
    def setUp(self) -> None:
        self.user1 = UserInfo.objects.create(
            email='test@test.com',
            name='Test',
            localization='Test123')

    def test_str_email(self):
        """ Test to return string of email label """
        self.assertEqual(self.user1.email, 'test@test.com')
