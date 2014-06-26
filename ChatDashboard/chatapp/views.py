from django.shortcuts import HttpResponse
from django.template import loader, RequestContext
from mongoengine.django.shortcuts import get_document_or_404
#from django.http import HttpResponse
from mongoengine.django.auth import *
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from mongoengine.django.sessions import *
from django.contrib.sessions.models import Session
from models import Message
from django.template import RequestContext, loader
import RegistrationFunctions
from datetime import datetime

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



def send_message(request):
    """Stub for send message test case"""
    return None

def register(request):
    if request.method == "POST":
        user = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        messages = []
        statuscode = 200
        
        
        if not RegistrationFunctions.validateEmail(email):
            messages.append("Invalid Email")
            statuscode = 400
        if not RegistrationFunctions.validatePassword(password):
            messages.append("Invalid Password")
            statuscode = 400

        
        if statuscode == 200:
            sessionUser =  get_user_model().objects.create_user(username=user, password=password, email=email)
            sessionUser.save()
            
            template = loader.get_template('Authentication/confirmregistration.html')
        else:
            template = loader.get_template('Authentication/registration.html')
            
        context = RequestContext(request, {'all_messages': messages, 'username':user, 'email':email})
        return HttpResponse( content=template.render(context), status=statuscode)
    else:
        template = loader.get_template('Authentication/registration.html')
        context = RequestContext(request, {
        'all_messages': None,
        })
        return HttpResponse(template.render(context))
    

def login_user(request):
    if request.method == "POST" and not request.user.is_authenticated():#and not request.user.is_authenticated(): #TODO: add in check for if user currently has a logged in session
       #request.session.create()
        usernm = request.POST['username']
        password = request.POST['password']
        messages = []
        statuscode = 400 # assume credentials are invalid
              
        #foundUser = User.objects.get(username=user)
           
        user = authenticate(username=usernm, password=password)
        #user = User.objects.get(username=usernm)
        if user is not None:
            # the password verified for the user
            if user.check_password(password):#user.is_active:
                    statuscode = 200
                    login(request, user)
                    #request.user.login(request, user)
                    
                    messages.append("User is valid, active and authenticated")
            else:
                    messages.append("The account has been disabled!")
        else:   
            # the authentication system was unable to verify the username and password
            messages.append("The username and password were incorrect.")        
        
        if statuscode == 200:
            context = RequestContext(request, {'all_messages': messages, 'authenticated': True })
        else:
            context = RequestContext(request, {'all_messages': messages,'authenticated': False })            
        
        template = loader.get_template('Authentication/login.html')
        return HttpResponse( content=template.render(context), status=statuscode)
    else:
       template = loader.get_template('Authentication/login.html')
       context = RequestContext(request, {'all_messages': None, 'authenticated': False} )        
    return HttpResponse(template.render(context))

def logoff_user(request):
    logout(request)
    request.session.delete()
    template = loader.get_template('Authentication/logoff.html')
    context = RequestContext(request, {'all_messages': None, 'authenticated': False} )  
    return HttpResponse(template.render(context))

from mongoengine.django.mongo_auth.models import MongoUserManager
from mongoengine.django.sessions import SessionStore
from mongoengine.django.sessions import MongoSession

#from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
def admin_functions(request):
    usernames = []
    userids = []
    
    if request.method=="POST" and request.POST['useraction']== "delete":
        rmvuser = request.POST['username']
        User.objects().filter(username=rmvuser).delete()
        
        users = User.objects.all()
        for user in users:
            usernames.append(user.username)
    
    #ursfound = User.objects.all()
    #if ursfound is not None: 
    #    for usr in ursfound:
    #        usernames.append(usr.username)
    
    if request.method=="POST" and request.POST['useraction']== "viewactiveusers":
        sessions = MongoSession.objects.all() #Session.objects.filter(expire_date__gte=datetime.now())
        for session in sessions:
            data = session.get_decoded()
            userids.append(data.get('_auth_user_id', None))
            #session.delete()
    
    
        for userid in userids:
            usr = get_user(userid)
            usernames.append(usr.username)
    

    if request.method=="POST" and request.POST['useraction']== "viewusers":
        #users = MongoEngineBackend().user_document().User.objects.all()
        users = User.objects.all()
        for user in users:
            usernames.append(user.username)
        

    template = loader.get_template('Authentication/currentusers.html')
    context = RequestContext(request, {'ursfound': usernames }) 
    return HttpResponse(template.render(context))

