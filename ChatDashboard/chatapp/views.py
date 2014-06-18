from django.shortcuts import HttpResponse
from django.template import loader, RequestContext
from mongoengine.django.shortcuts import get_document_or_404

from models import Dashboard

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
    template = loader.get_template('dashboard.html')
    dashboard = get_document_or_404(Dashboard, pk=title)
    context = RequestContext(request, {
        'dashboard': dashboard
    })
    return HttpResponse(template.render(context))