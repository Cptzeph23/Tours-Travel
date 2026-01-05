from django.shortcuts import render, redirect
from .models import Destination, Contact
from .forms import ContactForm
from django.contrib import messages

# Create your views here.

def index(request):
    dests = Destination.objects.all()
    return render(request, 'index.html', {'dests': dests})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # redirect to the same page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def news(request):
    return render(request, 'news.html')

def destinations(request):
    return render(request, 'destinations.html')

def gallery(request):
    return render(request, 'gallery.html')