from django.shortcuts import HttpResponse
from django.template import loader, RequestContext

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
