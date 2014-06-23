from django.conf.urls import patterns, include, url
#from django.views.generic import RedirectView

from django.contrib import admin
#from ChatDashboard.chatapp import views as caviews
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChatDashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/*', include(admin.site.urls)),
    #url(r'^$', RedirectView.as_view(url='/')),
    #url(r'Register/$', caviews.register),
    #url(r'AdminFunctions/$', caviews.admin_functions),
    #url(r'Login/$', caviews.login_user),
    #url(r'Logoff/$', caviews.logoff_user),
    url(r'^', include('chatapp.urls')),
)
