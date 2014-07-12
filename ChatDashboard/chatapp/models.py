#from django.db import models
from mongoengine import Document, StringField, DateTimeField, BooleanField

# Create your models here.
class Dashboard(Document):
    title = StringField(max_length=200, primary_key=True)
    creator = StringField(max_length=200)
    
class Dashboard_Permission(Document):
    dashboard_title = StringField(max_length=200)
    user = StringField(max_length=200)
    privilage = StringField(max_length=50) #values: user, admin

class Message(Document):
    msgtext = StringField(max_length=200)
    username = StringField(max_length=100)
    dashboardtitle = StringField(max_length=200)
    timestamp = DateTimeField()
    
class PasswordReset(Document):
    username = StringField(max_length=100)
    resetpin = StringField(max_length=200)
    time_issued = DateTimeField()
    time_expire = DateTimeField()
    used = BooleanField()