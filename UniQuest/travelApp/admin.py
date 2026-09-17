from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import BookingInquiry, Destination, GalleryItem, IndexDestination, Contact


class DestinationImageAdminForm(forms.ModelForm):
    # CloudinaryFileField's clearable widget evaluates value.url while the
    # form is rendering. FileInput intentionally does not evaluate the value,
    # which keeps local development independent of Cloudinary credentials.
    img = forms.FileField(required=False, label='Image', widget=forms.FileInput)

    class Meta:
        fields = '__all__'

    def clean_img(self):
        uploaded_image = self.cleaned_data.get('img')
        if uploaded_image:
            return uploaded_image
        if self.instance and self.instance.pk:
            return self.instance.img
        return uploaded_image


class IndexDestinationAdminForm(DestinationImageAdminForm):
    class Meta:
        model = IndexDestination
        fields = '__all__'


class DestinationAdminForm(DestinationImageAdminForm):
    class Meta:
        model = Destination
        fields = '__all__'


class GalleryAdminForm(DestinationImageAdminForm):
    image = forms.FileField(required=False, label='Media file', widget=forms.FileInput)

    class Meta:
        model = GalleryItem
        fields = '__all__'

    def clean_image(self):
        uploaded_media = self.cleaned_data.get('image')
        if uploaded_media:
            return uploaded_media
        if self.instance and self.instance.pk:
            return self.instance.image
        return uploaded_media


class DestinationAdminDisplayMixin:
    list_display = ('name', 'description_preview', 'price_display', 'image_preview')
    search_fields = ('name', 'desc')
    list_per_page = 25
    readonly_fields = ('current_image',)

    @admin.display(description='Description')
    def description_preview(self, obj):
        return obj.desc[:80] + ('…' if len(obj.desc) > 80 else '')

    @admin.display(description='Price', ordering='price')
    def price_display(self, obj):
        return f'${obj.price:,.2f}'

    @admin.display(description='Image')
    def image_preview(self, obj):
        if not obj.image_url:
            return 'No image'
        return format_html(
            '<img src="{}" alt="{}" style="width: 70px; height: 50px; '
            'object-fit: cover; border-radius: 4px;">',
            obj.image_url,
            obj.name,
        )

    @admin.display(description='Current image')
    def current_image(self, obj):
        if not obj.image_url:
            return 'No image uploaded.'
        return format_html(
            '<img src="{}" alt="{}" style="width: 120px; height: 85px; '
            'object-fit: cover; border-radius: 4px;">',
            obj.image_url,
            obj.name,
        )

    @admin.display(description='Key provisions')
    def provisions_preview(self, obj):
        provisions = obj.provision_list
        preview = ', '.join(provisions[:3])
        return preview + ('…' if len(provisions) > 3 else '')


@admin.register(IndexDestination)
class IndexDestinationAdmin(DestinationAdminDisplayMixin, admin.ModelAdmin):
    form = IndexDestinationAdminForm
    list_display = DestinationAdminDisplayMixin.list_display + ('display_order', 'offer')
    list_filter = ('offer',)
    ordering = ('display_order', 'id')
    fieldsets = (
        (None, {'fields': ('display_order', 'name', 'img', 'current_image', 'desc', 'price', 'offer')}),
    )


@admin.register(Destination)
class DestinationAdmin(DestinationAdminDisplayMixin, admin.ModelAdmin):
    form = DestinationAdminForm
    list_display = DestinationAdminDisplayMixin.list_display + ('display_order', 'subheading', 'provisions_preview')
    ordering = ('display_order', 'id')
    fieldsets = (
        (None, {'fields': ('display_order', 'name', 'img', 'current_image', 'subheading', 'desc', 'price', 'key_provisions')}),
    )


@admin.register(GalleryItem)
class GalleryItemAdmin(DestinationAdminDisplayMixin, admin.ModelAdmin):
    form = GalleryAdminForm
    list_display = ('name', 'media_type', 'description_preview', 'display_order', 'image_preview')
    list_filter = ('media_type',)
    ordering = ('display_order', 'id')
    search_fields = ('name', 'caption')
    readonly_fields = ('current_media',)
    fieldsets = (
        (None, {'fields': ('display_order', 'name', 'image', 'current_media', 'media_type', 'caption')}),
    )

    @admin.display(description='Description')
    def description_preview(self, obj):
        return obj.caption[:80] + ('…' if len(obj.caption) > 80 else '')

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if not obj.media_url:
            return 'No media'
        if obj.media_type == 'video':
            return format_html(
                '<video src="{}" style="width: 90px; height: 60px; object-fit: cover;" muted></video>',
                obj.media_url,
            )
        return format_html(
            '<img src="{}" alt="{}" style="width: 90px; height: 60px; object-fit: cover; border-radius: 4px;">',
            obj.media_url,
            obj.name,
        )

    @admin.display(description='Current media')
    def current_media(self, obj):
        return self.image_preview(obj)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(BookingInquiry)
class BookingInquiryAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'email', 'preferred_location', 'visit_date', 'number_of_people', 'budget_range', 'created_at')
    list_filter = ('budget_range', 'visit_date', 'created_at')
    search_fields = ('client_name', 'email', 'preferred_location', 'preferred_services', 'additional_requests')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
