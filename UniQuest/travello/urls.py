from  django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('destinations/', views.destinations, name='destinations'),
    path("sitemap.xml", TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml"))
]