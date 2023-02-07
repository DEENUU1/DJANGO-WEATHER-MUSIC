from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


# This function allows to send first welcome email after registration to newsletter

def send_email(template_name, username, email):
    template = render_to_string(template_name,
                                {'username': username})

    subject_email = 'Dziękujemy za rejestrację do newsletteru.'

    email = EmailMessage(
        subject_email,
        template,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email.fail_silently = False
    email.send()
