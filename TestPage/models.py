from django.db import models
from mongoengine import *

from TestSite2.settings import DBNAME

# Create your models here.
#mdbeng.connect(DBNAME)

class Message(Document):
    username = StringField(max_length=50, required=True)
    text = StringField(required=True)
    
class User(Document):
    username = StringField(max_length=50, required=True)
    password = StringField(max_length=50, required=True)
    email = StringField(mx_length=100, required=True)