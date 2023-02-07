from django.shortcuts import render, redirect
from .forms import RegisterForm, DeleteForm, NewsletterForm
from .models import UserInfo
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .mail import send_email


# This view works with NewsletterForm from forms.py and allows admin user to send a email
# For all registered users

@user_passes_test(lambda u: u.is_superuser)
def send_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():

            # sending email function
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')
            email_list = list(UserInfo.objects.values_list('email', flat=True))
            mail = EmailMessage(subject,
                                email_message,
                                settings.EMAIL_HOST_USER,
                                email_list,
                                bcc=receivers)
            mail.content_subtype = 'html'
            try:
                mail.send()
                print('email wysłany')
                messages.success(request, "Wiadomość została wysłana")
            except Exception as e:
                print('nie udało się')
                messages.error(request, "Nie udało się wysłać wiadomości: {}".format(e))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        return redirect("/")
    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in UserInfo.objects.all() if active.email])

    return render(request=request,
                  template_name='newsletter_form.html',
                  context={'form': form})


# This view is displaying form to register for newsletter

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if UserInfo.objects.filter(email=form.data['email']).exists():
            messages.error(request,
                           'Ten adres email jest już podany w bazie')
            return render(request,
                          'newsletter_register.html',
                          {'form': form})
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Dziękujemy za rejestrację do newslettera')

            # sending email after success registration to newsletter
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            send_email('newsletter_welcome.html',
                       name,
                       email)
        else:
            messages.error(request,
                           'Coś poszło nie tak. Spróbuj ponownie.')
    else:
        form = RegisterForm()
    return render(request,
                  'newsletter_register.html',
                  {'form': form})


# This view allows to delete newsletter subscription

def delete_view(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = UserInfo.objects.get(email=email)
                user.delete()
                messages.success(request,
                                 'Twoja subskrypcja została anulowana')
            except UserInfo.DoesNotExist:
                messages.error(request,
                               'Ten email nie istnieje')
    else:
        form = DeleteForm()
    return render(request,
                  'newsletter_delete.html',
                  {'form': form})




