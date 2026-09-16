from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse

from .models import Booking, Destination, GalleryItem, IndexDestination, Contact, Payment, Tour
from .forms import BookingForm, ContactForm

# Create your views here.

def index(request):
    dests = IndexDestination.objects.order_by('display_order', 'id')[:6]
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
    destinations = Destination.objects.order_by('display_order', 'id')
    return render(request, 'destinations.html', {'destinations': destinations})

def gallery(request):
    gallery_items = GalleryItem.objects.order_by('display_order', 'id')
    return render(request, 'gallery.html', {'gallery_items': gallery_items})


def robots_txt(request):
    content = (
        'User-agent: *\n'
        'Allow: /\n'
        'Disallow: /admin/\n'
        'Disallow: /accounts/\n'
        'Disallow: /booking/\n'
        f'Sitemap: {settings.SITE_URL}/sitemap.xml\n'
    )
    return HttpResponse(content, content_type='text/plain')

def maasaiVillage(request):
    return render(request, 'maasaiVillage.html')

def nairobiMuseum(request):
    return render(request, 'nairobiMuseum.html')

def kibraSlums(request):
    return render(request, 'kibra.html')

def coffeeFarm(request):
    return render(request, 'coffeeFarm.html')

def davidSheldrick(request):
    return render(request, 'davidSheldrick.html')

def giraffeCenter(request):
    return render(request, 'giraffeCentre.html')

def nairobiNationalPark(request):
    return render(request, 'nairobiPark.html')

def karenBlixen(request):
    return render(request, 'karenBlixen.html')

def nairobiCityTour(request):
    return render(request, 'nairobiTour.html')

def booking(request):
    return render(request, 'bookings.html')


#Price Calculation logic for booking form

def create_booking(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour

            #  Core logic
            booking.total_price = (
                tour.price_per_person * booking.number_of_people
            )

            booking.save()

            return redirect("initiate_payment", booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, "booking/form.html", {"form": form, "tour": tour})

# Payment success view to handle successful payments and update booking status
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = "paid"
    booking.save()

    Payment.objects.create(
        booking=booking,
        amount=booking.total_price,
        is_successful=True
    )

    send_booking_notification(booking)

    return render(request, "booking/success.html")
