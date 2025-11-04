from  django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('destinations/', views.destinations, name='destinations')
]