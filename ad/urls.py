from django.conf.urls import patterns, url

from .views import FlatAdDetailView
from .views import FlatAdListView
from .views import review
from .views import unreview

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flatsearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', FlatAdListView.as_view(), name='ad-list'),
    url(r'^(?P<pk>\d+)/$', FlatAdDetailView.as_view(), name='ad-detail'),
    url(r'^(?P<pk>\d+)/review$', review, name='ad-review'),
    url(r'^(?P<pk>\d+)/unreview$', unreview, name='ad-unreview'),
)
