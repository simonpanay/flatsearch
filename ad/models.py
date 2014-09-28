from django.db import models

from .references import City, FlatType, GES, Energy


class FlatAdManager(models.Manager):
    pass


class FlatAd(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=2, choices=City.CHOICES)
    zip_code = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    charges_included = models.NullBooleanField()
    flat_type = models.CharField(max_length=1, choices=FlatType.CHOICES)
    #'images': [thumb.split("url('")[1].split("');")[0].replace('thumbs', 'images') for thumb in tree.xpath('//div[@id="thumbs_carousel"]//span/@style')],
    furnished = models.NullBooleanField()
    area = models.PositiveIntegerField()
    ges = models.CharField(max_length=1, choices=GES.CHOICES, blank=True)
    energy_class = models.CharField(max_length=1, choices=Energy.CHOICES, blank=True)
    reviewed = models.BooleanField(default=False)
    objects = FlatAdManager()

    def __str__(self):
        return self.title
