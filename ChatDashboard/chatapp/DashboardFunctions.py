'''
Created on Jul 9, 2014

@author: Nick
'''
from models import Dashboard_Permission

def delete_dashboard_user(dashboard, user):
    successfull = False
    
    try: 
        dashboard_perm = Dashboard_Permission.objects.get(dashboard_title=dashboard, user=user)
        
        dashboard_perm.delete()
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
            dashboard_perm.privilage = Dashboard_Permissions.ADMIN
            dashboard_perm.save()
            successfull = True
        elif perm_level == Dashboard_Permissions.USER:            
            dashboard_perm.privilage = Dashboard_Permissions.USER
            dashboard_perm.save()
            successfull = True
    except:
        pass #will return false if permission is not found
    
    
    return successfull

def add_dashboard_user(dashboard, user, perm_level):
    successfull = False
    
    try: 
        # retrieve user. Uses objects.get so that it will error if there are multiple permissions
        dashboard_perm = Dashboard_Permission.objects.get(dashboard_title=dashboard, user=user)
        
        #will not throw error if the permission exists. In that case it should return as a failure.
    except:
        
        # only add permissions if the values are correct
        if perm_level == Dashboard_Permissions.ADMIN:
            dashboard_perm = Dashboard_Permission(dashboard_title=dashboard, user=user, privilage=Dashboard_Permissions.ADMIN)
            dashboard_perm.save()
            successfull = True
        elif perm_level == Dashboard_Permissions.USER:            
            dashboard_perm = Dashboard_Permission(dashboard_title=dashboard, user=user, privilage=Dashboard_Permissions.USER)
            dashboard_perm.save()
            successfull = True
    
    return successfull

class Dashboard_Permissions(object):
    ADMIN = "admin"
    USER = "user"
    
