from django.conf.urls import patterns, url
from chatapp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChatDashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'list/$', views.list, name="list"),
    url(r'Register/$', views.register),
    url(r'AdminFunctions/$', views.admin_functions),    
    url(r'AdminDashboardFunctions/$', views.admin_dashboard_functions),
    url(r'Login/$', views.login_user),
    url(r'Logoff/$', views.logoff_user),
    url(r'DashboardPermissions/$', views.dashboard_user_administration),
    url(r'PasswordFunctions/$', views.password_functions),
    url(r'(?P<title>\w+/?)$', views.render_dashboard, name="render_dashboard"),
    url(r'$', views.homepage),
)