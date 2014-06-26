from django.conf.urls import patterns, url
from chatapp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChatDashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'Register/$', views.register),
    url(r'AdminFunctions/$', views.admin_functions),
    url(r'Login/$', views.login_user),
    url(r'Logoff/$', views.logoff_user),
    #url(r'PasswordFunctions/(?P<function>\w{0,50})/$', views.password_functions),
    url(r'PasswordFunctions/$', views.password_functions),
    url(r'^(?P<title>\w+/?)$', views.render_dashboard, name="render_dashboard"),
    url(r'$', views.list, name="list"),
)