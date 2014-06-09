from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from models import Message
from django.template import RequestContext, loader


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

def register(address):
    """Stub for register test case"""
    return None

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