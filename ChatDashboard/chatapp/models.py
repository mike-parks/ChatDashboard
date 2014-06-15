#from django.db import models
from mongoengine import Document, StringField

# Create your models here.
class Dashboard(Document):
    title = StringField(max_length=200, primary_key=True)