from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .admin import DestinationAdmin, DestinationAdminForm, IndexDestinationAdmin
from .models import Destination, IndexDestination


class DestinationHomepageTests(TestCase):
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
