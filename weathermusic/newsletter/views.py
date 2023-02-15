from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm, DeleteForm, NewsletterForm
from .models import UserInfo


class SendNewsletterView(LoginRequiredMixin, UserPassesTestMixin, View):
    """ This view allows admin user to send newsletter for all registered users """

    form_class = NewsletterForm
    template_name = 'newsletter_form.html'

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
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
                messages.success(request, "Message was sent")
            except Exception as e:
                messages.error(request, "Failed to send message: {}".format(e))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        return redirect("/")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form.fields['receivers'].initial = ','.join([active.email for active in UserInfo.objects.all() if active.email])
        return render(request,
                      self.template_name,
                      {'form': form})


class SignUpView(View):
    """ This view allows user to register for newsletter """

    form_class = RegisterForm
    template_name = 'newsletter_register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if UserInfo.objects.filter(email=form.data['email']).exists():
            messages.error(request,
                           'This email is already registered')
            return render(request,
                          'newsletter_register.html',
                          {'form': form})

        if form.is_valid():
            form.save()
            messages.success(request,
                             'Your account has been created')
            return redirect('weather_music:main')
        else:
            messages.error(request,
                           'Account creation failed')

        return render(request, self.template_name, {'form': form})


class DeleteUserView(View):
    """ This view allows user to delete subscription in newsletter """

    template_name = 'newsletter_delete.html'
    form_class = DeleteForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = UserInfo.objects.get(email=email)
                user.delete()
                messages.success(request,
                                 'Account deleted')
                return redirect('weather_music:main')

            except UserInfo.DoesNotExist:
                messages.info(request,
                              'This account does not exist')
        else:
            messages.error(request, 'Account deletion failed')

        return render(request,
                      self.template_name,
                      {'form': form})
