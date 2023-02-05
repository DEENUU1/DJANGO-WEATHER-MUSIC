from django.shortcuts import render, redirect
from .forms import RegisterForm, DeleteForm
from .models import UserInfo
from django.contrib import messages

# This view is displaying form to register for newsletter


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'newsletter_successfully.html')
    else:
        form = RegisterForm()
    return render(request,
                  'newsletter_register.html',
                  {'form': form})


# This view is displaying form to delete newsletter


def delete_view(request):
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = UserInfo.objects.get(email=email)
                user.delete()
                return render(request, 'newsletter_deleted.html')
            except UserInfo.DoesNotExist:
                messages.error(request,
                               'Podany adress email nie istnieje')
    else:
        form = DeleteForm()
    return render(request,
                  'newsletter_delete.html',
                  {'form': form})
