from django.conf.urls import patterns, include, url

from django.contrib import admin
from TestPage.views import home
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TestSite2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'TestSite2.views.Home', name='home')
    url(r'hello/$', home),
)
