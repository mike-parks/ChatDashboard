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
        
        
        if not RegistrationFunctions.validate_email(email):
            messages.append("Invalid Email")
            statuscode = 400
        if not RegistrationFunctions.validate_password(password):
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

def homepage(request):
    print "Homepage"
    return login_user(request)

def login_user(request):
    print "Login user"
    if request.user.is_authenticated():
        return redirect('list/')
    if request.method == "POST" and not request.user.is_authenticated():#and not request.user.is_authenticated(): #TODO: add in check for if user currently has a logged in session
       #request.session.create()
        usernm = request.POST['username']
        password = request.POST['password']
        user = None
        messages = []
        error_messages = []
        statuscode = 400 # assume credentials are invalid
              
        try:
            foundUser = User.objects.get(username=usernm)
            user = authenticate(username=usernm, password=password)
        except:
            pass #pass becuase error message will be added below
            
        
        #if foundUser is not None:
        #    user = authenticate(username=usernm, password=password)
        #else:
        #    messages.append(usernm + " is already taken. Please try another username.")
            
        #user = User.objects.get(username=usernm)
        if user is not None:
            # the password verified for the user
            if user.check_password(password):
                    statuscode = 200
                    login(request, user)

                    messages.append("User is valid, active and authenticated")
                    return redirect('list/')
            else:
                    error_messages.append("Invalid Username/Password combination.")
        else:   
            # the authentication system was unable to verify the username and password
            error_messages.append("Invalid Username/Password combination.")        
        
        if statuscode == 200:
            context = RequestContext(request, {'messages': messages, 'authenticated': True, 'error_messages':error_messages})
        else:
            context = RequestContext(request, {'messages': messages,'authenticated': False , 'error_messages':error_messages})            
        
        template = loader.get_template('Authentication/login.html')
        return HttpResponse( content=template.render(context), status=statuscode)
    else:
       template = loader.get_template('Authentication/login.html')
       context = RequestContext(request, {'messages': None, 'authenticated': False, 'error_messages':None} )        
    return HttpResponse(template.render(context))

def logoff_user(request):
    logout(request)
    request.session.delete()
    template = loader.get_template('Authentication/logoff.html')
    context = RequestContext(request, {'messages': None, 'authenticated': False} )  
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
    context = None
    # handle posts
    if request.method == "POST" : 
        #handle change password request       
        if request.POST['password_action'] == "Change Password" :
            screen_title = "Change Password"
            username = request.POST["username"]
            current_password = request.POST["current_password"]
            new_password = request.POST["password"]
            
            screen_title = "Change Password"
            
            if validate_password(new_password):
                if change_password(username, current_password, new_password):
                    form_type = "sucessfullchange"
                    messages.append("Password successfully changed.")
                    form_type = "successfullchange"
                else:
                    error_messages.append("Invalid username/password combination.")
                    form_type = "changepassword"
            else:
                form_type = "changepassword"
                error_messages.append("Invalid password format.")
                
            
        #handle reset email request
        elif request.POST['password_action'] == "Reset Password": 
            generate_reset_email(request.POST['username'])
            form_type = "checkemail"
            screen_title = "Reset Password"
            messages.append("Please check your email for a password reset link.")
                
        #handle reset request with pin and username from email
        elif request.POST['password_action'] == "Reset My Password":
            screen_title = "Reset Password"
            username = request.POST['username']
            pin = request.POST['pin']
            password = request.POST['password']
            reset_error_message = reset_password(username, pin, password)
            if reset_error_message == None:
                form_type="successfulchange"
                messages.append("Password successfully reset.")
            else:                
                form_type = "resetpassword"
                error_messages.append("Password Reset Failed")
                error_messages.append(reset_error_message)
                
        # all gets that do not match a valid form_action should error
        else:
            screen_title = "ERROR"
            error_messages.append("Please use the appropriate link.")
    # handle gets
    else:
        if request.GET.get("function") == "changepassword":
            screen_title = "Change Password"
            form_type = "changepassword"
            
        #handle initial resetpasword link request 
        elif request.GET.get("function") =="resetpassword":
            screen_title = "Reset Password"
            form_type = "resetpassword"
            
        #handle reset password request from email link
        elif request.GET.get("function") =="resetpinsuccessful":
            screen_title = "Reset Password"
            username = request.GET.get("username")
            pin = request.GET.get('pin')
            form_type = "resetpinsuccessful"
            context = RequestContext(request, {'screen_title':screen_title , 'messages':messages, 'error_messages':error_messages, 'form_type': form_type, 'reset_username':username, 'reset_pin':pin })
        
        # all gets that do not match a valid function should errror
        else:
            screen_title = "ERROR"
            error_messages.append("Please use the appropriate link.")
    
    template = loader.get_template('Authentication/resetpassword.html')
    if context == None:
        context = RequestContext(request, {'screen_title':screen_title , 'messages':messages, 'error_messages':error_messages, 'form_type': form_type })
        
    return HttpResponse(template.render(context))
