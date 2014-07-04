from django.shortcuts import HttpResponse
from django.template import loader, RequestContext
from mongoengine.django.shortcuts import get_document_or_404
#from django.http import HttpResponse
from mongoengine.django.auth import *
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from RegistrationFunctions import *
import RegistrationFunctions

from models import Dashboard, Message
import datetime

# Create your views here.
def list(request):
    print "found list"
    print "Request: " + str(request)
    print "User logged in: " + str(auth.user_logged_in)

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
              
        foundUser = User.objects.get(username=usernm)
        
        if foundUser is not None:
            user = authenticate(username=usernm, password=password)
        else:
            messages.append(usernm + " is already taken. Please try another username.")
            
        #user = User.objects.get(username=usernm)
        if user is not None:
            # the password verified for the user
            if user.check_password(password):
                    statuscode = 200
                    login(request, user)

                    messages.append("User is valid, active and authenticated")
                    return redirect('list/')
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



#from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
def admin_functions(request):
    usernames = []
    userids = []
    
    if request.method=="POST" and request.POST['useraction']== "delete":
        rmvuser = request.POST['username']
        delete_user(rmvuser)
        usernames = retrieve_all_usernames()
    
    
    if request.method=="POST" and request.POST['useraction']== "viewactiveusers":
        usernames = retrieve_active_usernames()
    

    if request.method=="POST" and request.POST['useraction']== "viewusers":
        usernames = retrieve_all_usernames()
        

    template = loader.get_template('Authentication/currentusers.html')
    context = RequestContext(request, {'ursfound': usernames }) 
    return HttpResponse(template.render(context))

def password_functions(request):
    form_type = ""
    screen_title = ""
    error_messages = []
    messages = []
    if request.method == "POST" :        
        if request.POST['password_action'] == "Change Password" :
            screen_title = "Change Password"
            username = request.POST["username"]
            current_password = request.POST["current_password"]
            new_password = request.POST["password"]
            
            
            if change_password(username, current_password, new_password):
                form_type = "sucessfullchange"
                screen_title = "Change Password"
                messages.append("Password successfully changed.")
            else:
                error_messages.append("Invalid username/password combination.")
                screen_title = "Password Change Unsuccessful"
                
            
            form_type = "successfullchange"
        elif request.POST['password_action'] == "Reset Password":            
            form_type = "checkemail"
            screen_title = "Reset Password"
            messages.append("Please check your email for a password reset link.")
                
        else:
            screen_title = "ERROR"
            error_messages.append("Please use the appropriate link.")
    else:
        if request.GET.get("function") == "changepassword":
            screen_title = "Change Password"
            form_type = "changepassword"
        elif request.GET.get("function") =="resetpassword":
            screen_title = "Reset Password"
            form_type = "resetpassword"
        else:
            screen_title = "ERROR"
            error_messages.append("Please use the appropriate link.")
        
    send_email("bulls_eye_99@yahoo.com", "Test Message", "hi", )
    template = loader.get_template('Authentication/resetpassword.html')
    context = RequestContext(request, {'screen_title':screen_title , 'messages':messages, 'error_messages':error_messages, 'form_type': form_type })
        
    return HttpResponse(template.render(context))
