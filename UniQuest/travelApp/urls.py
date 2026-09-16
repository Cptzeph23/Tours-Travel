from  django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('news/', views.news, name='news'),
    path('destinations/', views.destinations, name='destinations'),
    path("robots.txt", views.robots_txt, name='robots_txt'),
    path('gallery/', views.gallery, name='gallery'),
    path('maasaiVillage/', views.maasaiVillage, name='maasaiVillage'),
    path('nairobiMuseum/', views.nairobiMuseum, name='nairobiMuseum'),
    path('kibraSlums/', views.kibraSlums, name='kibraSlums'),
    path('coffeeFarm/', views.coffeeFarm, name='coffeeFarm'),   
    path('davidSheldrick/', views.davidSheldrick, name='davidSheldrick'),
    path('giraffeCenter/', views.giraffeCenter, name='giraffeCenter'),
    path('nairobiPark/', views.nairobiNationalPark, name='nairobiPark'),
    path('karenBlixen/', views.karenBlixen, name='karenBlixen'),
    path('nairobiTour/', views.nairobiCityTour, name='nairobiTour'),
    path('booking/', views.booking, name='booking'),
    path("book/<int:tour_id>/", views.create_booking, name="create_booking"),
    
]
