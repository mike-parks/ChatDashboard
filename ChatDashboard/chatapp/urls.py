from django.conf.urls import patterns, include, url

from chatapp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChatDashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^(?P<dbid>\d+/?)$', views.render_dashboard),
    url(r'$', views.list),
)