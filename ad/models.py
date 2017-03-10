import collections
import datetime
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
            charges = raw_charges[0].strip()
        except:
            charges_included = None
        else:
            if charges == 'Charges comprises':
                charges_included = True
            else:
                charges_included = False
        return charges_included

    def get_ges(self, raw_info):
        try:
            ges = raw_info['ges'].upper()
        except:
            ges = ''
        return ges

    def get_nrj(self, raw_info):
        try:
            nrj = raw_info['nrj'].upper()
        except:
            nrj = ''
        return nrj

    def get_furnished(self, raw_info):
        try:
            furnished = raw_info['meuble']
        except:
            furnished = ''
        else:
            if furnished == 'non':
                furnished = False
            elif furnished == 'oui':
                furnished = True
            else:
                furnished = None
        return furnished

    def get_city(self, raw_info):
        try:
            city = raw_info['city']
        except:
            city = ''
        else:
            if city == 'grenoble':
                city = 'Grenoble'
            else:
                city = "Saint-Martin-d'Hères"
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

            raw_data = tree.xpath('//body/script[@type="text/javascript"]/text()')[0].strip().split('{')[1].strip("\n").split(',')
            data_lines = [option.strip().split(" : ") for option in raw_data]
            data_lines.pop()
            info = {line[0]: line[1].strip('"') for line in data_lines}

            try:
                raw_images = tree.xpath('//section[@class="adview_main"]/script/text()')[1].strip().split(';')
                images = ["".join(["http://", image.strip().split('//')[1].split('"')[0]]) for image in raw_images if image.strip().startswith('images[')]
            except:
                images = []

            ges = self.get_ges(info)
            nrj = self.get_nrj(info)
            furnished = self.get_furnished(info)
            description = "".join(["".join([line, "<br/><br/>"]) for line in tree.xpath('//div[@class="line properties_description"]/p[@id="description" or @itemprop="description"]/text()')])
            charges = tree.xpath('//h2[@class="item_price clearfix"]/span/span/text()')
            city = self.get_city(info)
            date = info['publish_date'].split('/')
            published = datetime.date(int(date[2]), int(date[1]), int(date[0]))
            date = info['last_update_date'].split('/')
            last_updated = datetime.date(int(date[2]), int(date[1]), int(date[0]))


            new_ad = self.create(
                pk = ad,
                title = info['titre'].replace('_', ' ').capitalize(),
                description = description,
                zip_code = int(info['cp']),
                price = int(info['loyer']),
                rooms = int(info['pieces']),
                charges_included = self.get_charges(charges),
                flat_type = info['type'],
                furnished = furnished,
                area = int(info['surface']),
                ges = ges,
                energy_class = nrj,
                city = city,
                published = published,
                last_updated = last_updated,
            )

            for image in images:
                new_ad.flatimage_set.create(url=image)

    def import_last_ads(self):
        ads = []
        for zip_code in ['38000', '38100', '38400']:
            payload = {
                'f': 'a',  # 
                'th': '1',  # 
                'mrs': '300',  # min price
                'mre': '700',  # max price
                'sqs': '5',  # min surface 
                'sqe': '8',  # max surface
                'ros': '1',  # min rooms
                'roe': '2',  # max rooms
                'ret': '1',  # house
                'ret': '2',  # appartment
                'furn': '2',  # furnished 1 yes 2 no
                'location': zip_code,  # zip code
            }
            search_url = os.path.join(LBC_URL, CATEGORY, OFFER, REGION, DEPARTMENT)
            page = requests.get(search_url, params=payload)
            tree = html.fromstring(page.text)
            ads_list = tree.xpath('/html/body/section/main/section/section/section/section/ul/li/a')
            ads = ads + [ad.items()[0][1].split('locations/')[1].split('.htm?')[0] for ad in ads_list]
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
    published = models.DateField()
    last_updated = models.DateField()
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
    ad = models.OneToOneField(FlatAd)
    street = models.CharField(max_length=255)

    def __str__(self):
        return self.street

    def get_absolute_url(self):
        return reverse('ad:ad-detail', kwargs={'pk': self.ad.pk})

    def map_link(self):
        return " ".join(["https://www.google.fr/maps/preview?q=", self.street, self.ad.city])
