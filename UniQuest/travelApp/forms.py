from django import forms
from django.utils import timezone

from travelApp.models import Booking, BookingInquiry, Contact


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


class BookingInquiryForm(forms.ModelForm):
    class Meta:
        model = BookingInquiry
        fields = (
            'client_name', 'email', 'preferred_location', 'visit_date',
            'number_of_people', 'budget_range', 'preferred_services',
            'additional_requests',
        )
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'preferred_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'For example: Maasai Mara, Nairobi, Diani'}),
            'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'budget_range': forms.Select(attrs={'class': 'form-control'}),
            'preferred_services': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Safari, airport transfer, accommodation, guide, etc.'}),
            'additional_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Accessibility needs, dietary requirements, amenities, or any other request.'}),
        }

    def clean_visit_date(self):
        visit_date = self.cleaned_data['visit_date']
        if visit_date < timezone.localdate():
            raise forms.ValidationError('Please select today or a future date.')
        return visit_date
