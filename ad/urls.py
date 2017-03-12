from django.conf.urls import url

from .views import UserCriteriaCreateView
from .views import UserCriteriaDeleteView
from .views import UserCriteriaListView
from .views import UserCriteriaUpdateView
from .views import FlatAdDetailView
from .views import FlatAdListView
from .views import review
from .views import interesting
from .views import notinteresting
from .views import unreview
from .views import update_ads
from .views import AddressCreateView
from .views import AddressUpdateView

urlpatterns = [
    url(r'^$', FlatAdListView.as_view(), name='ad-list'),
    url(r'^update$', update_ads, name='ad-list-update'),
    url(r'^(?P<pk>\d+)/$', FlatAdDetailView.as_view(), name='ad-detail'),
    url(r'^(?P<pk>\d+)/address$', AddressCreateView.as_view(), name='ad-create-address'),
    url(r'^updateaddress/(?P<pk>\d+)$', AddressUpdateView.as_view(), name='ad-update-address'),
    url(r'^(?P<pk>\d+)/review$', review, name='ad-review'),
    url(r'^(?P<pk>\d+)/unreview$', unreview, name='ad-unreview'),
    url(r'^(?P<pk>\d+)/interesting$', interesting, name='ad-interesting'),
    url(r'^(?P<pk>\d+)/notinteresting$', notinteresting, name='ad-notinteresting'),
    url(r'^criterias$', UserCriteriaListView.as_view(), name='user-criteria-list'),
    url(r'^criterias/add$', UserCriteriaCreateView.as_view(), name='user-criteria-create'),
    url(r'^criterias/(?P<pk>\d+)/update$', UserCriteriaUpdateView.as_view(), name='user-criteria-update'),
    url(r'^criterias/(?P<pk>\d+)/delete$', UserCriteriaDeleteView.as_view(), name='user-criteria-delete'),
]
