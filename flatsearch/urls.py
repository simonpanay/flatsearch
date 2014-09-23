from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flatsearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ad/', include('ad.urls', namespace='ad')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
)
