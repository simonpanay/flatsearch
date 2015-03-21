import collections
import os
import requests

from django.core.urlresolvers import reverse
from django.db import models

from .references import City, FlatType, GES, Energy

from lxml import html


LBC_URL = "http://www.leboncoin.fr"
CATEGORY = "locations"
REGION = "rhone_alpes"
DEPARTMENT = "isere"
OFFER = "offres"


class FlatAdManager(models.Manager):
    def get_charges(self, raw_charges):
        try:
            charges = raw_charges[0]
        except:
            charges_included = None
        else:
            if charges == 'Oui':
                charges_included = True
            else:
                charges_included = False
        return charges_included

    def get_ges(self, raw_ges):
        try:
            ges = raw_ges[0]
        except:
            ges = ''
        else:
            ges = ges[0].split()[0]
        return ges

    def get_energy(self, raw_energy):
        try:
            energy = raw_energy[0]
        except:
            energy = ''
        else:
            energy = energy[0].split()[0]
        return energy

    def get_furnished(self, raw_furnished):
        try:
            furnished = raw_furnished[0]
        except:
            furnished = None
        else:
            if furnished == 'Non meublé':
                furnished = False
            elif furnished == 'Meublé':
                furnished = True
            else:
                furnished = None
        return furnished

    def get_city(self, raw_city):
        try:
            city = raw_city[0]
        except:
            city = ''
        return city

    def get_flat_type(self, raw_flat_type):
        try:
            flat_type = raw_flat_type[0]
        except:
            flat_type = ''
        else:
            if flat_type == 'Appartement':
                flat_type = 'f'
            else:
                flat_type = 'h'
        return flat_type

    def create_ad(self, ad):
        if not self.filter(pk=ad).exists():
            detail_url = os.path.join(LBC_URL, CATEGORY, str(ad) + ".htm")
            page = requests.get(detail_url)
            tree = html.fromstring(page.text)
            charges = self.get_charges(tree.xpath('//*[child::*[contains(text(), "Charges comprises :")]]/td/text()'))
            ges = self.get_ges(tree.xpath('//*[child::*[contains(text(), "GES :")]]/td/noscript/a/text()'))
            energy_class = self.get_energy(tree.xpath('//*[child::*[contains(text(), "Classe énergie :")]]/td/noscript/a/text()'))
            furnished = self.get_furnished(tree.xpath('//*[child::*[contains(text(), "Meublé / Non meublé :")]]/td/text()'))
            city = self.get_city(tree.xpath('//*[child::*[contains(text(), "Ville :")]]/td/text()'))
            flat_type = self.get_flat_type(tree.xpath('//*[child::*[contains(text(), "Type de bien :")]]/td/text()'))
            images = [thumb.split("url('")[1].split("');")[0].replace('thumbs', 'images') for thumb in tree.xpath('//div[@id="thumbs_carousel"]//span/@style')],
            description = tree.xpath('//div[@class="AdviewContent"]//div[@class="content"]/text()')
            description = "<br>".join([line for line in description])
            new_ad = self.create(
                pk = ad,
                title = tree.xpath('//h2[@id="ad_subject"]/text()')[0],
                description = description,
                zip_code = int(tree.xpath('//*[child::*[contains(text(), "Code postal :")]]/td/text()')[0]),
                price = tree.xpath('//span[@class="price"]/text()')[0].split()[0],
                rooms = int(tree.xpath('//*[child::*[contains(text(), "Pièces :")]]/td/text()')[0]),
                charges_included = charges,
                flat_type = flat_type,
                furnished = furnished,
                area = tree.xpath('//*[child::*[contains(text(), "Surface :")]]/td/text()')[0].split()[0],
                ges = ges,
                energy_class = energy_class,
                city = city,
            )
            for image in images[0]:
                new_ad.flatimage_set.create(url=image)

    def import_last_ads(self):
        ads = []
        for zip_code in ['38000', '38100', '38400']:
            payload = {
                'f': 'a',  # 
                'th': '1',  # 
                'mrs': '300',  # min price
                'mre': '700',  # max price
                'sqs': '3',  # min surface 
                'sqe': '7',  # max surface
                'ros': '2',  # min rooms
                'roe': '3',  # max rooms
                'ret': '1',  # house
                'ret': '2',  # appartment
                #'furn': '2',  # furnished 1 yes 2 no
                'location': zip_code,  # zip code
            }
            search_url = os.path.join(LBC_URL, CATEGORY, OFFER, REGION, DEPARTMENT)
            page = requests.get(search_url, params=payload)
            tree = html.fromstring(page.text)
            ads_list = tree.xpath('//div[@class="list-lbc"]//a/@href')
            ads_list.pop()
            ads = ads + [ad.split('locations/')[1].split('.htm?')[0] for ad in ads_list]
        for ad in ads:
            self.create_ad(ad)


class FlatAd(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=255)
    zip_code = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    charges_included = models.NullBooleanField()
    flat_type = models.CharField(max_length=1, choices=FlatType.CHOICES)
    furnished = models.NullBooleanField()
    area = models.PositiveIntegerField()
    ges = models.CharField(max_length=1, choices=GES.CHOICES, blank=True)
    energy_class = models.CharField(max_length=1, choices=Energy.CHOICES, blank=True)
    reviewed = models.BooleanField(default=False)
    interesting = models.BooleanField(default=False)
    objects = FlatAdManager()

    class Meta:
        ordering = ['-interesting', 'reviewed', '-pk']

    def __str__(self):
        return '{} - {} - {}'.format(self.pk,
                                     self.city,
                                     self.title)

    def get_absolute_url(self):
        return reverse('ad:ad-detail', kwargs={'pk': self.pk})

    def url(self):
        return os.path.join(LBC_URL, CATEGORY, str(self.pk) + ".htm")

    def review(self):
        self.reviewed = True
        self.save()

    def mark_interesting(self):
        self.interesting = True
        self.reviewed = True
        self.save()

    def mark_notinteresting(self):
        self.interesting = False
        self.save()

    def unreview(self):
        self.reviewed = False
        self.save()

    def price_per_square_meter(self):
        return round(self.price / self.area, 1)


class FlatImage(models.Model):
    ad = models.ForeignKey(FlatAd)
    url = models.URLField(max_length=255)


class Street(models.Model):
    ad = models.ForeignKey(FlatAd, unique=True)
    street = models.CharField(max_length=255)

    def __str__(self):
        return self.street

    def get_absolute_url(self):
        return reverse('ad:ad-detail', kwargs={'pk': self.ad.pk})

    def map_link(self):
        return " ".join(["https://www.google.fr/maps/preview?q=", self.street, self.ad.city])
