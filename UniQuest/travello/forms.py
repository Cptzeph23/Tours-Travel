from django import forms

from travello.models import Booking, Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']



#Booking form to handle tour bookings

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "full_name",
            "email",
            "phone",
            "visit_date",
            "visit_time",
            "number_of_people",
        ]