from django.core.management.base import BaseCommand, CommandError
from restaurants.models import RestaurantLocation


class Command(BaseCommand):
    help = 'Create the restaurant'

    def add_arguments(self, parser):
        parser.add_argument('restaurant_name', type=str)

    def handle(self, *args, **options):
        try:
            restaurants =  RestaurantLocation.objects.search(options['restaurant_name'])
            for restaurant in restaurants:
                print('-----------------')
                print('Name: {}\nLocation: {}\nCategory: {}'.format(restaurant.name, restaurant.location, restaurant.category))
        except RestaurantLocation.DoesNotExist:
            raise CommandError('{} does not exist'.format(options['restaurant_name']))
        self.stdout.write(self.style.SUCCESS('Retrieved {} data successfully '.format(options['restaurant_name'])))
