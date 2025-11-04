from django.shortcuts import render
from .models import Destination

# Create your views here.

def index(request):
    dests = Destination.objects.all()
    return render(request, 'index.html', {'dests': dests})

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def news(request):
    return render(request, 'news.html')

def destinations(request):
    return render(request, 'destinations.html')