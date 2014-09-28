import collections
import os
import requests

from django.db import models

from .references import City, FlatType, GES, Energy

from lxml import html


LBC_URL = "http://www.leboncoin.fr"
CATEGORY = "locations"
REGION = "rhone_alpes"
DEPARTMENT = "isere"
OFFER = "offres"


class FlatAdManager(models.Manager):
    def import_last_ads(self):
        payload = {
            'f': 'a',  # 
            'th': '1',  # 
            'mrs': '300',  # min price
            'mre': '600',  # max price
            'sqs': '3',  # min surface 
            'sqe': '6',  # max surface
            'ros': '2',  # min rooms
            'roe': '3',  # max rooms
            'ret': '1',  # house
            'ret': '2',  # appartment
            #'furn': '2',  # furnished 1 yes 2 no
            'location': '38400',  # zip code
        }
        search_url = os.path.join(LBC_URL, CATEGORY, OFFER, REGION, DEPARTMENT)
        page = requests.get(search_url, params=payload)
        tree = html.fromstring(page.text)
        ads_list = tree.xpath('//div[@class="list-lbc"]//a/@href')
        ads = [ad.split('locations/')[1].split('.htm?')[0] for ad in ads_list]
        for ad in ads:
            if not self.filter(pk=ad).exists():
                detail_url = os.path.join(LBC_URL, CATEGORY, str(ad) + ".htm")
                page = requests.get(detail_url)
                self.create_ad(ad, page)

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
            city = raw_city[0][0]
        except:
            city = ''
        else:
            if city == 'Grenoble':
                city = 'gr'
            else:
                city = 'sm'
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

    def create_ad(self, ad, page):
        tree = html.fromstring(page.text)
        charges = self.get_charges(tree.xpath('//*[child::*[contains(text(), "Charges comprises :")]]/td/text()'))
        ges = self.get_ges(tree.xpath('//*[child::*[contains(text(), "GES :")]]/td/noscript/a/text()'))
        energy_class = self.get_energy(tree.xpath('//*[child::*[contains(text(), "Classe énergie :")]]/td/noscript/a/text()'))
        furnished = self.get_furnished(tree.xpath('//*[child::*[contains(text(), "Meublé / Non meublé :")]]/td/text()'))
        city = self.get_city(tree.xpath('//*[child::*[contains(text(), "Ville :")]]/td/text()'))
        flat_type = self.get_flat_type(tree.xpath('//*[child::*[contains(text(), "Type de bien :")]]/td/text()'))
        new_ad = self.create(
            pk = ad,
            title = tree.xpath('//h2[@id="ad_subject"]/text()')[0],
            description = tree.xpath('//div[@class="AdviewContent"]//div[@class="content"]/text()'),
            zip_code = int(tree.xpath('//*[child::*[contains(text(), "Code postal :")]]/td/text()')[0]),
            price = tree.xpath('//span[@class="price"]/text()')[0].split()[0],
            #images = [thumb.split("url('")[1].split("');")[0].replace('thumbs', 'images') for thumb in tree.xpath('//div[@id="thumbs_carousel"]//span/@style')],
            rooms = int(tree.xpath('//*[child::*[contains(text(), "Pièces :")]]/td/text()')[0]),
            charges_included = charges,
            flat_type = flat_type,
            furnished = furnished,
            area = tree.xpath('//*[child::*[contains(text(), "Surface :")]]/td/text()')[0].split()[0],
            ges = ges,
            energy_class = energy_class,
            city = city,
        )


class FlatAd(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=2, choices=City.CHOICES)
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
    objects = FlatAdManager()

    def __str__(self):
        return '{} - {}'.format(self.pk, self.title)
