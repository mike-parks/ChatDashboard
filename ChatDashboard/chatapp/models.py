#from django.db import models
from mongoengine import Document, StringField, DateTimeField, BooleanField

# Create your models here.
class Dashboard(Document):
    title = StringField(max_length=200, primary_key=True)

class Message(Document):
    msgtext = StringField(max_length=200)
    dashboardtitle = StringField(max_length=200)
    timestamp = DateTimeField()
    
class PasswordReset(Document):
    username = StringField(max_length=100)
    resetpin = StringField(max_length=200)
    time_issued = DateTimeField()
    time_expire = DateTimeField()
    used = BooleanField()