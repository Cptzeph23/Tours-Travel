from django.db import models  # type: ignore
from django.db.models import Max
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from cloudinary.models import CloudinaryField  # type: ignore
import uuid
from pathlib import Path
# Create your models here.


class DestinationImageField(CloudinaryField):
    """Use local Django storage in development and Cloudinary in production."""

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not settings.USE_CLOUDINARY and isinstance(value, UploadedFile):
            storage = FileSystemStorage(
                location=settings.DESTINATION_UPLOAD_ROOT,
                base_url=settings.DESTINATION_UPLOAD_URL,
            )
            stored_name = storage.save(f'uploads/destinations/{value.name}', value)
            setattr(model_instance, self.attname, stored_name)
            return stored_name
        return super().pre_save(model_instance, add)


class DestinationImageMixin:
    @property
    def image_url(self):
        """Return the local or production image URL for the destination."""
        if not self.img:
            return ''
        public_id = getattr(self.img, 'public_id', str(self.img))
        if public_id.startswith('uploads/destinations/'):
            storage = FileSystemStorage(
                location=settings.DESTINATION_UPLOAD_ROOT,
                base_url=settings.DESTINATION_UPLOAD_URL,
            )
            if storage.exists(public_id):
                return storage.url(public_id)

            relative_path = Path(public_id)
            try:
                _, files = storage.listdir(str(relative_path.parent))
            except FileNotFoundError:
                files = []
            for filename in files:
                if Path(filename).stem == relative_path.name:
                    return storage.url(str(relative_path.parent / filename))
            return ''
        if not settings.USE_CLOUDINARY:
            return ''
        try:
            return self.img.url
        except ValueError:
            return ''


class IndexDestination(DestinationImageMixin, models.Model):
    name = models.CharField(max_length=100)
    img = DestinationImageField(
        'image',
        folder='destinations',  # Organize images in a folder
        use_filename=True,      # Use original filename
        unique_filename=False,  # Don't make unique if same filename
        overwrite=True          # Overwrite if same filename
    )
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(
        default=0,
        help_text='Lower numbers appear first. Ties use the original ID order.',
    )

    class Meta:
        ordering = ('display_order', 'id')

    def save(self, *args, **kwargs):
        if self._state.adding and self.display_order == 0:
            self.display_order = (type(self).objects.aggregate(max_order=Max('display_order'))['max_order'] or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Destination(DestinationImageMixin, models.Model):
    name = models.CharField(max_length=100)
    img = DestinationImageField(
        'image',
        folder='destinations',
        use_filename=True,
        unique_filename=False,
        overwrite=True,
    )
    subheading = models.CharField(max_length=180, default='')
    desc = models.TextField()
    price = models.IntegerField()
    key_provisions = models.TextField(
        default='',
        help_text='Enter one key provision per line.'
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text='Lower numbers appear first. Ties use the original ID order.',
    )

    class Meta:
        ordering = ('display_order', 'id')

    def save(self, *args, **kwargs):
        if self._state.adding and self.display_order == 0:
            self.display_order = (type(self).objects.aggregate(max_order=Max('display_order'))['max_order'] or 0) + 1
        super().save(*args, **kwargs)

    @property
    def provision_list(self):
        return [item.strip() for item in self.key_provisions.splitlines() if item.strip()]

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

# Bookings model to store tour bookings
class Tour(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    




class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    visit_date = models.DateField()
    visit_time = models.TimeField()

    number_of_people = models.PositiveIntegerField()

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.tour.title}"


# Payment model to handle payments for bookings
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
