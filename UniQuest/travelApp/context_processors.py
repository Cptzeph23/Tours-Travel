import json

from django.conf import settings


SITE_NAME = 'UniQuest Tours & Travels'
DEFAULT_DESCRIPTION = (
    'UniQuest Tours & Travels offers authentic Kenya tours, safaris, travel experiences, '
    'and cultural adventures from Nairobi.'
)

PAGE_METADATA = {
    '/': (
        'UniQuest Tours & Travels | Kenya Safaris, Tours & Travel Experiences',
        'Discover Kenya with UniQuest Tours & Travels: Nairobi safaris, cultural tours, wildlife experiences, and memorable travel adventures.',
    ),
    '/about/': ('About UniQuest Tours & Travels | Kenya Travel Experts', 'Learn about UniQuest Tours & Travels, a Kenya-based travel company creating authentic safaris, tours, and cultural experiences.'),
    '/destinations/': ('Kenya Tour Destinations | UniQuest Tours & Travels', 'Explore Kenya tour destinations including Nairobi, Maasai Mara, Amboseli, coastal experiences, museums, and cultural attractions.'),
    '/gallery/': ('Kenya Travel Gallery | UniQuest Tours & Travels', 'View photos and videos from UniQuest Tours & Travels safaris, Kenya tours, wildlife encounters, and cultural travel experiences.'),
    '/contact/': ('Contact UniQuest Tours & Travels | Kenya Tours', 'Contact UniQuest Tours & Travels to plan a Kenya safari, Nairobi tour, cultural experience, or custom travel itinerary.'),
    '/news/': ('Kenya Travel News & Tour Updates | UniQuest Tours & Travels', 'Read Kenya travel news, safari updates, destination inspiration, and practical advice from UniQuest Tours & Travels.'),
    '/nairobiPark/': ('Nairobi National Park Tour | UniQuest Tours & Travels', 'Plan a Nairobi National Park safari with UniQuest Tours & Travels for wildlife viewing, game drives, and expert local guidance.'),
    '/nairobiTour/': ('Nairobi City Tour | UniQuest Tours & Travels', 'Explore Nairobi’s wildlife, history, culture, and landmarks with a guided Nairobi city tour from UniQuest Tours & Travels.'),
    '/giraffeCenter/': ('Giraffe Centre Visit | UniQuest Tours & Travels', 'Experience the Giraffe Centre in Nairobi with UniQuest Tours & Travels and meet endangered Rothschild giraffes up close.'),
    '/davidSheldrick/': ('David Sheldrick Wildlife Trust Tour | UniQuest Tours', 'Visit Nairobi conservation attractions with UniQuest Tours & Travels, including the David Sheldrick Wildlife Trust experience.'),
    '/karenBlixen/': ('Karen Blixen Museum Tour | UniQuest Tours & Travels', 'Discover the Karen Blixen Museum and Nairobi heritage experiences with UniQuest Tours & Travels.'),
    '/coffeeFarm/': ('Kenya Coffee Farm Tour | UniQuest Tours & Travels', 'Discover Kenya coffee growing, harvesting, processing, and tasting on a guided coffee farm tour.'),
    '/kibraSlums/': ('Kibra Cultural Tour | UniQuest Tours & Travels', 'Experience a respectful, community-led Kibra cultural tour with UniQuest Tours & Travels.'),
    '/maasaiVillage/': ('Maasai Village Cultural Tour | UniQuest Tours', 'Discover Maasai culture, heritage, and community traditions on a guided Kenya cultural tour.'),
    '/nairobiMuseum/': ('Nairobi National Museum Tour | UniQuest Tours', 'Explore Kenya’s history, art, science, and cultural heritage at the Nairobi National Museum with UniQuest Tours & Travels.'),
}


def seo(request):
    path = request.path if request.path.endswith('/') else f'{request.path}/'
    title, description = PAGE_METADATA.get(
        path,
        ('Kenya Tours & Safaris | UniQuest Tours & Travels', DEFAULT_DESCRIPTION),
    )
    canonical = f'{settings.SITE_URL}{path}'
    structured_data = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'TravelAgency',
                '@id': f'{settings.SITE_URL}/#organization',
                'name': SITE_NAME,
                'url': settings.SITE_URL,
                'description': DEFAULT_DESCRIPTION,
                'areaServed': 'Kenya',
                'sameAs': [
                    'https://www.facebook.com/profile.php?id=61583113811233',
                    'https://www.instagram.com/uniquestadventure/',
                ],
            },
            {
                '@type': 'WebSite',
                '@id': f'{settings.SITE_URL}/#website',
                'name': SITE_NAME,
                'url': settings.SITE_URL,
                'publisher': {'@id': f'{settings.SITE_URL}/#organization'},
            },
        ],
    }
    return {
        'seo': {
            'title': title,
            'description': description,
            'canonical': canonical,
            'image': f'{settings.SITE_URL}/static/images/home_slider.jpg',
            'structured_data': json.dumps(structured_data),
        }
    }
