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
            
        if foundUser > 0:
            messages.append("Please choose another username.")
            statuscode = 400
        
        
        if statuscode == 200:
            template = loader.get_template('Authentication/confirmregistration.html')
        else:
            template = loader.get_template('Authentication/registration.html')
            
        context = RequestContext(request, {'all_messages': messages, })
        return HttpResponse( content=template.render(context), status=statuscode)
    else:
        template = loader.get_template('Authentication/registration.html')
        context = RequestContext(request, {
        'all_messages': None,
        })
        return HttpResponse(template.render(context))

def login(address):
    """Stub for login test case"""
    return None

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