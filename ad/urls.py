from django.conf.urls import patterns, url

from ad.views import prout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flatsearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', prout, name='prout'),
)
