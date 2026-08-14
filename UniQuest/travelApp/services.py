from django.core.mail import send_mail
from django.conf import settings

def send_booking_notification(booking):
    subject = f"New Booking for {booking.tour.title}"

    message = f"""
    A new booking has been made.

    Name: {booking.full_name}
    Email: {booking.email}
    Phone: {booking.phone}

    Tour: {booking.tour.title}
    Location: {booking.tour.location}

    Date: {booking.visit_date}
    Time: {booking.visit_time}

    People: {booking.number_of_people}
    Total Paid: {booking.total_price}
    """

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ["owner@email.com"])