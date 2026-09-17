import json
import logging
from urllib import error, request

from django.core.mail import send_mail
from django.conf import settings


logger = logging.getLogger(__name__)

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


def _send_resend_email(recipient, subject, text, reply_to=None):
    """Send one email through Resend's HTTP API without an extra dependency."""
    if not all((settings.RESEND_API_KEY, settings.RESEND_FROM_EMAIL, recipient)):
        logger.warning('Resend email not sent: configuration or recipient is missing.')
        return False

    sender = f'{settings.RESEND_FROM_NAME} <{settings.RESEND_FROM_EMAIL}>'
    payload = {'from': sender, 'to': [recipient], 'subject': subject, 'text': text}
    if reply_to:
        payload['reply_to'] = reply_to
    api_request = request.Request(
        'https://api.resend.com/emails',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {settings.RESEND_API_KEY}',
            'Content-Type': 'application/json',
            'User-Agent': 'UniQuest-Tours-Travel/1.0',
        },
        method='POST',
    )
    try:
        with request.urlopen(api_request, timeout=settings.RESEND_TIMEOUT) as response:
            return 200 <= response.status < 300
    except error.HTTPError as exc:
        response_body = exc.read().decode('utf-8', errors='replace')
        logger.error('Resend email delivery failed with HTTP %s: %s', exc.code, response_body)
        return False
    except (error.URLError, TimeoutError) as exc:
        logger.error('Resend email delivery failed: %s', exc)
        return False


def send_booking_inquiry_emails(inquiry):
    """Notify the team and acknowledge the customer after an inquiry is saved."""
    details = (
        f'Name: {inquiry.client_name}\nEmail: {inquiry.email}\n'
        f'Preferred location: {inquiry.preferred_location}\nVisit date: {inquiry.visit_date}\n'
        f'Number of people: {inquiry.number_of_people}\nBudget: {inquiry.get_budget_range_display()}\n'
        f'Preferred services: {inquiry.preferred_services or "Not specified"}\n'
        f'Additional requests: {inquiry.additional_requests or "None"}\n'
    )
    _send_resend_email(
        settings.BOOKING_NOTIFICATION_EMAIL,
        f'New UniQuest booking inquiry: {inquiry.preferred_location}',
        f'A new booking inquiry has been received.\n\n{details}',
        reply_to=inquiry.email,
    )
    if settings.BOOKING_COPY_TO_CUSTOMER:
        _send_resend_email(
            inquiry.email,
            'We received your UniQuest booking inquiry',
            f'Hello {inquiry.client_name},\n\nThank you for contacting UniQuest Tours & Travels. '
            f'We received your request and will get back to you shortly.\n\nYour booking details:\n{details}\n'
            'Kind regards,\nUniQuest Tours & Travels',
        )
