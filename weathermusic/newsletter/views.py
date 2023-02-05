from django.shortcuts import render
from .forms import NewsLetterForm


# This view is displaying form to register for newsletter

def register_view(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'newsletter_successfully.html')
    else:
        form = NewsLetterForm()
    return render(request,
                  'newsletter_register.html',
                  {'form': form})