
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', include('travelApp.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'))
]

if settings.DEBUG or not settings.USE_CLOUDINARY:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
