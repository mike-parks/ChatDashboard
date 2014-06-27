'''
Created on Jun 13, 2014

@author: Nick
'''
import re
from mongoengine.django.sessions import MongoSession
from mongoengine.django.auth import *
from mongoengine.django.sessions import *

def validateEmail(email):
    regex_pattern = "[^@]+@[^@]+\.[^@]+"
    re.compile(regex_pattern)
    
    if not re.match(regex_pattern, email):
        return False
    else:
        return True
    
def validatePassword(password):
    regex_pattern = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    re.compile(regex_pattern)
    
    if not re.match(regex_pattern, password):
        return False
    else:
        return True
    
def retrieve_active_usernames():
    userids = []
    usernames = []
    
    sessions = MongoSession.objects.all() #Session.objects.filter(expire_date__gte=datetime.now())
    for session in sessions:
        data = session.get_decoded()
        userids.append(data.get('_auth_user_id', None))
    
    
    for userid in userids:
        usr = get_user(userid)
        usernames.append(usr.username)
        
    return usernames

def retrieve_all_usernames():
    usernames = []
    
    users = User.objects.all()
    for user in users:
        usernames.append(user.username)
            
    return usernames

def check_for_active_users(usernames):    
    active_usernames = retrieve_active_usernames()
    
    matched_usernames = list(set(usernames) & set(active_usernames))
    
    #for a_user in active_usernames:
    #    for b_user in usernames:
    #        if a_user == b_user:
    #            matched_usernames.append(b_user)
    
    return matched_usernames

def delete_user(username):
    User.objects().filter(username=username).delete()
    
def change_password(username, current_password, new_password):
    user = User.objects.get(username=username)
    
    if user.check_password(current_password):
        user.set_password(new_password)
        return True
    else:
        return False
   
import os
from models import PasswordReset
import datetime
def generate_reset_email(username):
    email = ""
    
    #send email to email address associated with their username
    user = User.objects.filter(username=username)
    if user == None:
        return False
    else:
        email = user[1].email
    
    pin = os.urandom(32)
    url = "%sPasswordFunctions/?function=resetpassword&username=%s&pin=%s" %(settings.BASE_URL, username, pin)
    
    message = "Please Click the following URL to reset your password:\n%s" %(url)

    #add reset stats to database
    current_timestamp =  DateTimeField(default=datetime.datetime.now)
    exptime = datetime.datetime.now + datetime.timedelta(minutes=30) 
    expire_timestamp = DateTimeField(default=exptime)
    passwordreset = PasswordReset(username=username, resetpin=pin, time_issued=current_timestamp, time_expire=expire_timestamp, used=False )
    passwordreset.save()

    send_email(email, "ChatDashboard Password Reset", message)

    return True

def check_password_reset(username, pin):
    valid_pin = False
    current_timestamp =  DateTimeField(default=datetime.datetime.now)
    
    passwordreset = PasswordReset(username=username, resetpin=pin, time_issued__gte=current_timestamp, time_expire__lt=current_timestamp, used=False)
    for resetpin in passwordreset:
        resetpin.used = True
        resetpin.save()
        valid_pin = True
    
    return valid_pin

import smtplib 
from email.mime.text import MIMEText
from ChatDashboard import settings
def send_email(email, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_FROMADDRESS
    msg['To']=email
    
    server = smtplib.SMTP(settings.EMAIL_SERVER, settings.EMAIL_PORT)
    server.sendmail(settings.EMAIL_FROMADDRESS, email, msg.as_string())
    server.quit()
    
    
    
    