import os
import requests

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from lxml import html


LBC_URL = "http://www.leboncoin.fr"
CATEGORY = "locations"
REGION = "rhone_alpes"
DEPARTMENT = "isere"
OFFER = "offres"


# Create your views here.
def ads_list(request):
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
        'furn': '2',  # furnished 1 yes 2 no
        'location': '38400',  # zip code
    }
    search_url = os.path.join(LBC_URL, CATEGORY, OFFER, REGION, DEPARTMENT)
    page = requests.get(search_url, params=payload)
    tree = html.fromstring(page.text)
    ads_list = tree.xpath('//div[@class="list-lbc"]//a/@href')
    ads = [ad.split('locations/')[1].split('.htm?')[0] for ad in ads_list]
    return render_to_response('ad/ad_list.html',
                              {'ads_list': ads},
                              context_instance=RequestContext(request))



def ad_detail(request, pk):
    detail_url = os.path.join(LBC_URL, CATEGORY, str(pk) + ".htm")
    page = requests.get(detail_url)
    tree = html.fromstring(page.text)
    charges = tree.xpath('//*[child::*[contains(text(), "Charges comprises :")]]/td/text()'),
    if len(charges) > 0:
        charges_included = charges[0]
    else:
        charges_included = None
    reference = tree.xpath('//*[child::*[contains(text(), "Référence :")]]/td/text()'),
    if reference[0]:
        ref = reference[0][0]
    else:
        ref = None
    _ges = tree.xpath('//*[child::*[contains(text(), "GES :")]]/td/noscript/a/text()'),
    if _ges[0]:
        ges = _ges[0][0].split()[0]
    else:
        ges = None
    energy = tree.xpath('//*[child::*[contains(text(), "Classe énergie :")]]/td/noscript/a/text()'),
    if energy[0]:
        energy_class = energy[0][0].split()[0]
    else:
        energy_class = None
    ad = {
        'description': tree.xpath('//div[@class="AdviewContent"]//div[@class="content"]/text()'),
        'town': tree.xpath('//*[child::*[contains(text(), "Ville :")]]/td/text()')[0],
        'zip_code': int(tree.xpath('//*[child::*[contains(text(), "Code postal :")]]/td/text()')[0]),
        'price': tree.xpath('//span[@class="price"]/text()')[0].split()[0],
        'images': [thumb.split("url('")[1].split("');")[0].replace('thumbs', 'images') for thumb in tree.xpath('//div[@id="thumbs_carousel"]//span/@style')],
        'rooms': int(tree.xpath('//*[child::*[contains(text(), "Pièces :")]]/td/text()')[0]),
        'charges_included': charges_included,
        'type': tree.xpath('//*[child::*[contains(text(), "Type de bien :")]]/td/text()')[0],
        'furnished': tree.xpath('//*[child::*[contains(text(), "Meublé / Non meublé :")]]/td/text()')[0],
        'area': tree.xpath('//*[child::*[contains(text(), "Surface :")]]/td/text()')[0].split()[0],
        'ref': ref,
        'ges': ges,
        'energy_class': energy_class,
    }
    return render_to_response('ad/ad_detail.html',
                              {'ad': ad},
                              context_instance=RequestContext(request))
