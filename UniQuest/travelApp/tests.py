from datetime import timedelta

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone

from .admin import DestinationAdmin, DestinationAdminForm, GalleryItemAdmin, IndexDestinationAdmin
from .models import BookingInquiry, Destination, GalleryItem, IndexDestination


class DestinationHomepageTests(TestCase):
    def test_homepage_has_search_metadata_and_structured_data(self):
        response = self.client.get('/')

        self.assertContains(response, 'UniQuest Tours &amp; Travels | Kenya Safaris, Tours &amp; Travel Experiences')
        self.assertContains(response, 'rel="canonical" href="https://www.uniquesttravels.tours/"')
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, 'TravelAgency')

    def test_robots_and_sitemap_expose_public_pages(self):
        robots_response = self.client.get('/robots.txt')
        sitemap_response = self.client.get('/sitemap.xml')

        self.assertEqual(robots_response.status_code, 200)
        self.assertEqual(robots_response['Cache-Control'], 'no-store, max-age=0, must-revalidate')
        self.assertContains(robots_response, 'Allow: /')
        self.assertContains(robots_response, 'Disallow: /admin/')
        self.assertContains(robots_response, 'Sitemap: https://www.uniquesttravels.tours/sitemap.xml')
        self.assertEqual(sitemap_response.status_code, 200)
        self.assertContains(sitemap_response, 'http://testserver/destinations/')
        self.assertContains(sitemap_response, 'http://testserver/gallery/')

    @override_settings(DEBUG=True, USE_CLOUDINARY=False)
    def test_destination_image_is_saved_to_local_assets_in_development(self):
        destination = IndexDestination.objects.create(
            name='Local destination',
            img=SimpleUploadedFile('lake.jpg', b'fake image contents', content_type='image/jpeg'),
            desc='A local test destination.',
            price=25,
        )
        self.addCleanup(
            FileSystemStorage(location=settings.DESTINATION_UPLOAD_ROOT).delete,
            destination.img,
        )

        self.assertTrue(destination.img.startswith('uploads/destinations/'))
        self.assertIn('/static/uploads/destinations/', destination.image_url)

    def test_destination_is_rendered_from_database(self):
        IndexDestination.objects.create(
            name='Lake Naivasha',
            img='',
            desc='Boat rides and beautiful wildlife views.',
            price=75,
        )

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lake Naivasha')
        self.assertContains(response, 'Boat rides and beautiful wildlife views.')
        self.assertContains(response, '$75.00')
        self.assertNotContains(response, 'Nairobi National Park')

    def test_homepage_renders_at_most_six_index_destinations(self):
        for number in range(1, 8):
            IndexDestination.objects.create(
                name=f'Index destination {number}',
                img='',
                desc='Homepage description.',
                price=number * 10,
            )

        response = self.client.get('/')

        self.assertContains(response, 'Index destination 1')
        self.assertContains(response, 'Index destination 6')
        self.assertNotContains(response, 'Index destination 7')

    def test_display_order_controls_both_destination_pages(self):
        IndexDestination.objects.create(name='Second', img='', desc='Second.', price=20, display_order=2)
        IndexDestination.objects.create(name='First', img='', desc='First.', price=10, display_order=1)
        Destination.objects.create(
            name='Main second', img='', subheading='', desc='Second.', price=20,
            key_provisions='', display_order=2,
        )
        Destination.objects.create(
            name='Main first', img='', subheading='', desc='First.', price=10,
            key_provisions='', display_order=1,
        )

        index_response = self.client.get('/')
        destinations_response = self.client.get('/destinations/')

        self.assertLess(index_response.content.index(b'First'), index_response.content.index(b'Second'))
        self.assertLess(destinations_response.content.index(b'Main first'), destinations_response.content.index(b'Main second'))

    def test_destination_admin_has_image_preview(self):
        self.assertIn('image_preview', DestinationAdmin.list_display)
        self.assertIn('description_preview', DestinationAdmin.list_display)
        self.assertIn('image_preview', IndexDestinationAdmin.list_display)

    def test_admin_change_form_does_not_evaluate_cloudinary_url(self):
        destination = Destination(
            name='Existing destination',
            img='uploads/destinations/existing.jpg',
            subheading='Existing subheading',
            desc='Existing description.',
            price=40,
            key_provisions='Guided visits\nBottle of water',
        )

        form = DestinationAdminForm(instance=destination)

        self.assertIn('name="img"', form.as_p())

    def test_destinations_page_renders_unlimited_main_destinations(self):
        Destination.objects.create(
            name='Main destination',
            img='',
            subheading='A memorable experience',
            desc='Main destination description.',
            price=150,
            key_provisions='Guided visits\nBottle of water',
        )

        response = self.client.get('/destinations/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Main destination')
        self.assertContains(response, 'A memorable experience')
        self.assertContains(response, 'Guided visits')

    def test_gallery_page_renders_admin_managed_items_in_order(self):
        GalleryItem.objects.create(
            name='Second gallery item', image='', caption='Second caption', display_order=2,
        )
        GalleryItem.objects.create(
            name='First gallery item', image='', caption='First caption', display_order=1,
        )

        response = self.client.get('/gallery/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First gallery item')
        self.assertContains(response, 'Second gallery item')
        self.assertLess(response.content.index(b'First gallery item'), response.content.index(b'Second gallery item'))
        self.assertIn('image_preview', GalleryItemAdmin.list_display)


class BookingInquiryTests(TestCase):
    booking_data = {
        'client_name': 'Amina Otieno',
        'email': 'amina@example.com',
        'preferred_location': 'Maasai Mara',
        'visit_date': '2030-08-14',
        'number_of_people': 3,
        'budget_range': '100_250',
        'preferred_services': 'Safari guide and airport transfer',
        'additional_requests': 'Vegetarian meals',
    }

    def test_booking_request_is_saved_and_confirmation_is_rendered(self):
        response = self.client.post('/booking/', self.booking_data)

        self.assertRedirects(response, '/booking/confirmation/1/')
        inquiry = BookingInquiry.objects.get()
        confirmation = self.client.get(response.url)
        self.assertContains(confirmation, 'Request received')
        self.assertContains(confirmation, inquiry.preferred_location)
        self.assertContains(confirmation, inquiry.preferred_services)

    def test_booking_request_rejects_a_past_visit_date(self):
        response = self.client.post(
            '/booking/',
            {**self.booking_data, 'visit_date': (timezone.localdate() - timedelta(days=1)).isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please select today or a future date.')
        self.assertFalse(BookingInquiry.objects.exists())
