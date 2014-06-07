from django.db import models
import mongoengine as mdbeng

from TestSite2 import DBNAME

# Create your models here.
mdbeng.connect(DBNAME)

class Post(Document):
    username = mdbeng.StringField(max_length=50, required=True)
    message = mdbeng.StringField(max_length=10000, required=True)