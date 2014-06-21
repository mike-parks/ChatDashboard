from django.shortcuts import HttpResponse
from django.template import loader, RequestContext
from mongoengine.django.shortcuts import get_document_or_404

from models import Dashboard, Message
import datetime

# Create your views here.
def list(request):
    print "found list"
    if request.method == "POST":
        title = request.POST['title']
        dashboard = Dashboard(title=title)
        dashboard.save()

    all_dashboards = Dashboard.objects()
    template = loader.get_template('list.html')
    context = RequestContext(request, {
        'all_dashboards': all_dashboards
    })
    return HttpResponse(template.render(context))

def render_dashboard(request, title):
    if request.method == "POST":
        message = request.POST.get('message', '')
        dashboard_title = request.POST['dashboard_title']
        message = Message(msgtext=message, timestamp=datetime.datetime.now(), dashboardtitle=dashboard_title)
        message.save()

    messages_here = Message.objects(dashboardtitle=title)
    template = loader.get_template('dashboard.html')
    dashboard = get_document_or_404(Dashboard, pk=title)
    context = RequestContext(request, {
        'all_messages': messages_here,
        'dashboard': dashboard
    })
    return HttpResponse(template.render(context))