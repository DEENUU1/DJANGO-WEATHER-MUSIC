from django.shortcuts import render, redirect
from .forms import RegisterForm, DeleteForm
from .models import UserInfo
from django.contrib import messages
import os
from dotenv import load_dotenv
from mailerlite import MailerLiteApi


load_dotenv()

# This view is displaying form to register for newsletter


def register_view(request):
    if request.method == 'POST':

        email = request.POST['email']
        name = request.POST['name']

        mailchimpClient = Client()
        mailchimpClient.set_config({
            "api_key": os.getenv('MAILCHIMP_API_KEY'),
        })

        userInfo = {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": name,
            }
        }

        list_id = os.getenv('LIST_ID')
        try:
            mailchimpClient.lists.add_list_member(list_id, userInfo)
            return redirect("newsletter:success")
        except ApiClientError:
            return redirect("newsletter:error")

    return render(request, "newsletter_register.html")


def success(request):
    return render(request, "newsletter_successfully.html")


def error(request):
    return render(request, "newsletter_error.html")


