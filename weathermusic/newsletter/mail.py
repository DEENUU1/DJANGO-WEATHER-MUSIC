from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


# Email subject is static and can be modified only here

def send_email(template_name: str, username: str, email: str):
    """ This function allows to send welcome email for registered users """

    template = render_to_string(template_name,
                                {'username': username})

    subject_email = 'Dziękujemy za rejestrację do newslettera.'

    email = EmailMessage(
        subject_email,
        template,
        settings.EMAIL_HOST_USER,
        [email],
    )

    email.fail_silently = False
    email.send()
