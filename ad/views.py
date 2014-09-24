import requests

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from lxml import html


LE_BON_COIN_URL = "http://www.leboncoin.fr"


# Create your views here.
def ads_list(request):
    payload = {
        'f': 'a',
        'th': '1',
        'mrs': '300',
        'mre': '600',
        'sqs': '3',
        'sqe': '6',
        'ros': '2',
        'roe': '3',
        'ret': '1',
        'ret': '2',
        'furn': '2',
        'location': '38000',
    }
    page = requests.get(LE_BON_COIN_URL + "/locations/offres/rhone_alpes/isere/", params=payload)
    tree = html.fromstring(page.text)
    ads_list = tree.xpath('//div[@class="list-lbc"]//a/@href')
    ads = [ad.split('locations/')[1].split('.htm?')[0] for ad in ads_list]
    return render_to_response('ad/ad_list.html',
                              {'ads_list': ads},
                              context_instance=RequestContext(request))



def ad_detail(request, pk):
    page = requests.get(LE_BON_COIN_URL + "/locations/" + str(pk) + ".htm")
    tree = html.fromstring(page.text)
    price = tree.xpath('//span[@class="price"]/text()')
    thumbs = tree.xpath('//div[@id="thumbs_carousel"]//span/@style')
    images = [thumb.split("url('")[1].split("');")[0].replace('thumbs', 'images') for thumb in thumbs]
    return render_to_response('ad/ad_detail.html',
                              {'price': price,
                               'images': images,},
                              context_instance=RequestContext(request))
