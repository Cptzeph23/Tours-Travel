from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .models import Booking, Destination, Contact, Payment, Tour
from .forms import BookingForm, ContactForm

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


