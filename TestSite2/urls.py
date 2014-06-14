from django.conf.urls import patterns, include, url

from django.contrib import admin
import TestPage.views as tpv
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TestSite2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'TestSite2.views.Home', name='home')
    url(r'hello/$', tpv.home),
    url(r'second/$', tpv.secondfunction),
    url(r'^$', tpv.create),
    url(r'Register/$', tpv.register),
    url(r'AdminFunctions/$', tpv.admin_functions),
)
