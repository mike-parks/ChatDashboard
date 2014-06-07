from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from models import Message

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
    '''
    if request.method == "POST":
        username = request.POST['username']
        text = request.POST['text']
        message = Message(username=username)
        message.text = text
        message.save()
    '''

    all_messages = Message.objects().first().text
    return HttpResponse(all_messages)