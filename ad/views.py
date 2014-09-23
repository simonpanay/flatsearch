import requests

from django.shortcuts import render, redirect

from lxml import html

# Create your views here.
def prout(request):
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
    page = requests.get("http://www.leboncoin.fr/locations/offres/rhone_alpes/isere/", params=payload)
    tree = html.fromstring(page.text)
    ads_list = tree.xpath('//a/@href')
    ads = [ad for ad in ads_list if 'location' in ad]
    print(ads)
