from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Destination, IndexDestination, Contact


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

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
