'''
Created on Jul 9, 2014

@author: Nick
'''
from models import Dashboard_Permission, Dashboard, Message, Topic
from mongoengine.django.auth import *
from RegistrationFunctions import send_email

def delete_dashboard_user(dashboard, user):
    successfull = False
    
    try: 
        dashboard_perm = Dashboard_Permission.objects.get(dashboard_title=dashboard, user=user)
        
        dashboard_perm.delete()
        successfull = True
    except:
        pass #will return false if permission is not found
    
    return successfull

def change_dashboard_permissions(dashboard, user, perm_level):
    successfull = False
    
    try: 
        # retrieve user. Uses objects.get so that it will error if there are multiple permissions
        dashboard_perm = Dashboard_Permission.objects.get(dashboard_title=dashboard, user=user)

        # only add permissions if the values are correct
        if perm_level == Dashboard_Permissions.ADMIN:
            dashboard_perm.privilege = Dashboard_Permissions.ADMIN
            dashboard_perm.save()
            successfull = True
        elif perm_level == Dashboard_Permissions.USER:            
            dashboard_perm.privilege = Dashboard_Permissions.USER
            dashboard_perm.save()
            successfull = True
    except:
        pass #will return false if permission is not found
    
    
    return successfull

def send_add_dashboard_email(dashboard, user, email, perm_level):
    message = "Congratulations, {}! You have been granted {} access to the {} Dashboard.".format(user, perm_level, dashboard)
    
    user_object = User.objects.filter(username=user)
    
    if (len(user_object)== 1):
        send_email(email, "Chat Dashboard Access Granted", message)
    

def add_dashboard_user(dashboard, user, perm_level):
    successfull = False
    
    try: 
        # retrieve user. Uses objects.get so that it will error if there are multiple permissions
        dashboard_perm = Dashboard_Permission.objects.filter(dashboard_title=dashboard, user=user)
        users = User.objects.filter(username=user)
        
        if len(dashboard_perm) == 0 and len(users) == 1:
            email = user[0].email
            
            # confirm that a valid permission level is being assigned
            if perm_level == Dashboard_Permissions.ADMIN:
                dashboard_perm = Dashboard_Permission(dashboard_title=dashboard, user=user, privilege=Dashboard_Permissions.ADMIN)
                dashboard_perm.save()
                successfull = True # set to true first, because we want it to return true as long as the permissions are added, even if the email fails
                send_add_dashboard_email(dashboard, user, email, perm_level)
            elif perm_level == Dashboard_Permissions.USER:            
                dashboard_perm = Dashboard_Permission(dashboard_title=dashboard, user=user, privilege=Dashboard_Permissions.USER)
                dashboard_perm.save()
                send_add_dashboard_email(dashboard, user, email, perm_level)
                successfull = True # set to true first, because we want it to return true as long as the permissions are added, even if the email fails
                send_add_dashboard_email(dashboard, user, email, perm_level)
        
        #will not throw error if the permission exists. In that case it should return as a failure.
    except:
        
        # only add permissions if the values are correct
        if perm_level == Dashboard_Permissions.ADMIN:
            dashboard_perm = Dashboard_Permission(dashboard_title=dashboard, user=user, privilege=Dashboard_Permissions.ADMIN)
            dashboard_perm.save()
            successfull = True
        elif perm_level == Dashboard_Permissions.USER:            
            dashboard_perm = Dashboard_Permission(dashboard_title=dashboard, user=user, privilege=Dashboard_Permissions.USER)
            dashboard_perm.save()
            successfull = True
    
    return successfull

def delete_dashboard(dashboard):
    successfull = True

    #delete dashboard
    dboards = Dashboard.objects.filter(title=dashboard)
    #dboards = Dashboard.objects.filter(pk=dashboard)
    
    if len(dboards) > 0:
        for dboard in dboards:
            dboard.delete()
    else: 
        successfull = False
    
    #delete user permissions
    dperms = Dashboard_Permission.objects.filter(dashboard_title=dashboard)
    if len(dperms) > 0:
        for dperm in dperms:
            dperm.delete()
    else:
    #    print("\"" + dashboard + "\" failed to delete")
    #    for dper in Dashboard_Permission.objects:
    #        print("\"" + dper.dashboard_title + "\"")
        successfull = False
        
    dtopics = Topic.objects.filter(dashboard_title=dashboard)
    if len(dtopics) > 0:
        for dtopic in dtopics:
            dtopic.delete()
    
    #delete messages: note may not always have messages
    dmessages = Message.objects.filter(dashboardtitle=dashboard)
    if len(dmessages) > 0:
        for dmessage in dmessages:
            dmessage.delete()
            
    return successfull

def add_topic_window(topicname, dashboardname):
    to_save_topic = True
    
    topic_windows = Topic.objects.filter(topic_title=topicname, dashboard_title=dashboardname)
      
    if len(topic_windows) > 0:
        to_save_topic = False
    #for topic_window in topic_woindows:
    #    if topic_window.topic_title == topicname:
    #        to_save_topic = False

    if to_save_topic:
        topic = Topic(topic_title = topicname,
                      topic_active = True,
                      dashboard_title = dashboardname)
        topic.save()
    return to_save_topic

def deactivate_topic_window(topicname, dashboardname):
    deactivated_topic = False
    
    topic_windows = Topic.objects.filter(topic_title=topicname, dashboard_title=dashboardname)
    
    for topic_window in topic_windows:
        topic_window.topic_active = False
        topic_window.save()
        deactivated_topic = True


    return deactivated_topic

class Dashboard_Permissions(object):
    ADMIN = "admin"
    USER = "user"
    
