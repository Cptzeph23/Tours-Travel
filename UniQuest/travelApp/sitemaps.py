from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticPagesSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return (
            'index', 'about', 'destinations', 'gallery', 'contact', 'news',
            'nairobiPark', 'nairobiTour', 'giraffeCenter',
            'davidSheldrick', 'karenBlixen', 'coffeeFarm', 'kibraSlums',
            'maasaiVillage', 'nairobiMuseum',
        )

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'index' else 0.8 if item in ('destinations', 'gallery') else 0.6
