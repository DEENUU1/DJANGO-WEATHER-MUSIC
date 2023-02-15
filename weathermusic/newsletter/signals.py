from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import UserInfo


@receiver(post_save, sender=UserInfo)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        template = render_to_string('newsletter_welcome.html',
                                    {'name':instance.name})

        subject_email = 'Dziękujemy za rejestrację do newslettera.'

        email = EmailMessage(
            subject_email,
            template,
            settings.EMAIL_HOST_USER,
            [instance.email],
        )

        email.fail_silently = False
        email.send()

