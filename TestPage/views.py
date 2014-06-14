from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from models import Message
from models import User
from django.template import RequestContext, loader
import RegistrationFunctions


def home(request):
    return HttpResponse("Hello, World")


def secondfunction(request):
    print_string = "Request is %s" % str(request)
    #return HttpResponse("Second function info")
    return HttpResponse(print_string)


def create(request):
    """If we have a POST, sends the data to Mongo.
    Each POST must have a username string and message string.
    Then displays all Mongo contents on webpage."""
    print "found create"
    if request.method == "POST":
        username = request.POST['username']
        text = request.POST['text']
        message = Message(username=username)
        message.text = text
        message.save()

    all_messages = Message.objects()
    template = loader.get_template('TestPage/index.html')
    context = RequestContext(request, {
        'all_messages': all_messages,
    })
    return HttpResponse(template.render(context))

from django.contrib.auth.models import User
def register(request):
    """Stub for register test case"""
    print "Found Register"
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
        

        foundUser = User.objects.filter(username=user)
            
        if foundUser.count() > 0:
            messages.append("Please choose another username.")
            statuscode = 400
        
        
        
        
        
        if statuscode == 200:
            sessionUser = User.objects.create_user(user, email, password)
            user.save()
            
            new_user = User(username=user, email=email)
            #new_user = User(username=user, password=password, email=email)
            #new_user.save()
            #request.session["user"] = user
            #request.session["authenticated"] = True
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
    
from django.contrib.auth import authenticate
def login_user(request):
    """Stub for login test case"""
    if request.method == "POST" and not request.user.is_authenticated(): #TODO: add in check for if user currently has a logged in session
        user = request.POST['username']
        password = request.POST['password']
        messages = []
        statuscode = 400 # assume credentials are invalid
              
        #foundUser = User.objects.get(username=user)
           
        user = authenticate(username='john', password='secret')
        if user is not None:
            # the password verified for the user
            if user.is_active:
                    statuscode = 200
                    request.user.login(request, user)
                    messages.append("User is valid, active and authenticated")
            else:
                    messages.append("The account has been disabled!")
        else:   
            # the authentication system was unable to verify the username and password
            messages.append("The username and password were incorrect.")
            
       # if foundUser:
       #     if foundUser.password == password:
        #        statuscode = 200
        
        
        if statuscode == 200:
            request.session["user"] = user
            request.session["authenticated"] = True
            context = RequestContext(request, {'all_messages': messages, 'authenticated': True })
        else:
            context = RequestContext(request, {'all_messages': messages,'authenticated': False })            
        
        template = loader.get_template('Authentication/login.html')
        return HttpResponse( content=template.render(context), status=statuscode)
    else:
       template = loader.get_template('Authentication/login.html')
       context = RequestContext(request, {'all_messages': None, 'authenticated': False} )        
    return HttpResponse(template.render(context))

def logout(address):
    """Stub for logout test case"""
    return None

def changePassword(address):
    """Stub for Change Password test case"""
    return None

def email(address):
    """Stub for email test case"""
    return None


def send_message(request):
    """Stub for send message test case"""
    return None

def admin_functions(request):
    
    template = loader.get_template('Authentication/currentusers.html')
    all_users = User.objects()
    context = RequestContext(request, {
        'all_users': all_users,
        })
    return HttpResponse(template.render(context))