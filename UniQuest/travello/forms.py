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

        widgets = {
            "visit_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "visit_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "number_of_people": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }