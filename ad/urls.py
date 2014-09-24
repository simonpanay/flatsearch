from django.conf.urls import patterns, url

from ad.views import ads_list
from ad.views import ad_detail

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flatsearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', ads_list, name='ad-list'),
    url(r'^(?P<pk>\d+)/$', ad_detail, name='ad-detail'),
)
