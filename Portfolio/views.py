from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

# Create your views here.
def index(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + '  Email: ' + from_email
            try:
                send_mail(subject, message, from_email, ['loevliedenny@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('Portfolio:success')
    return render(request, 'Portfolio/index.html', {'form': form})
    # return render(request,'Portfolio/index.html')

def timeline(request):
    return render(request, 'Portfolio/timeline.html')


def portfolio(request):
    return render(request, 'Portfolio/portfolio.html')


def blog(request):
    return render(request, 'Portfolio/blog.html')