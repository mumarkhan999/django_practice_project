from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.db.models import Q

from .utils import unique_slug_generator
from .validators import validate_category

User = settings.AUTH_USER_MODEL


class RestaurantLocationQuerySet(models.query.QuerySet):
    def search(self, query):
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) |
                Q(category__icontains=query) |
                Q(item__name__icontains=query) |
                Q(item__contents__icontains=query)
            ).distinct()
        return self


class RestaurantLocationManager(models.Manager):
    def get_queryset(self):
        return RestaurantLocationQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class RestaurantLocation(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True, null=True)
    category = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])
    # first time
    timestamp = models.DateTimeField(auto_now_add=True)
    # every time
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)
    objects = RestaurantLocationManager()

    def get_absolute_url(self):
        return reverse('restaurants:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return 'Name: ({})   Location: ({})   Category: ({})    Owner: ({})'.format(self.name, self.location,
                                                                                    self.category, self.owner)

    @property
    def title(self):
        return self.name


def rl_pre_save_reciever(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    instance.location = instance.location.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


# def rl_post_save_reciever(sender, instance, *args, **kwargs):
#    print('saved')
#    print(instance.timestamp)
#    if not instance.slug:
#        instance.slug = unique_slug_generator(instance)
#        instance.save()

pre_save.connect(rl_pre_save_reciever, sender=RestaurantLocation)

# post_save.connect(rl_post_save_reciever, sender=RestaurantLocation)
