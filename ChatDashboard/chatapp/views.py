from django.shortcuts import HttpResponse
from django.template import loader, RequestContext
from mongoengine.django.shortcuts import get_document_or_404
#from django.http import HttpResponse
from mongoengine.django.auth import *
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from RegistrationFunctions import *
import RegistrationFunctions
from DashboardFunctions import *
from MetricsReportFunctions import *
from django.http import HttpResponseRedirect
import TopicWindowFunctions

from models import Dashboard, Message, Dashboard_Permission
import datetime

# Create your views here.
def list(request):
    #print "found list"
    #print "Request: " + str(request)
    #print "User logged in: " + str(request.user.is_authenticated())#str(auth.user_logged_in)
    messages = []
    error_messages = []
    
    if (not request.user.is_authenticated()):
        return redirect(settings.BASE_URL)

    username = request.user.username
#should check to make sure dashboard doesn't already exist
    if request.method == "POST":
        try:
            if request.POST["create_dashboard_submit"] == "Create Chat Dashboard":
                title = request.POST['title'].strip()
                dashboard = Dashboard(title=title, creator=username)
                permission = Dashboard_Permission(dashboard_title=title, user=username, privilege=Dashboard_Permissions.ADMIN)
                to_save = True
                for dash in Dashboard.objects:
                    if dash.title == title:
                        to_save = False
           
                    if to_save:
                        dashboard.save()
                        permission.save()
                        print "Created Dashboard: " + title
                    else:
                        messages.append("Cannot create dashboard - the dashboard already exists")
        except:
            try:
                if request.POST["invite_user_submit"] == "Invite User":
                    invite_user(request.POST["inviteemail"],username)
            except:
                pass

    user_dashboards = None
    try:
        user_dashboards = Dashboard_Permission.objects.filter(user=username)
    except:
        messages.append("You are not a user on any Dashboards.")
        
    all_dashboards = Dashboard.objects()
    template = loader.get_template('list.html')
    context = RequestContext(request, {
        'all_dashboards': all_dashboards,
        'user_dashboards': user_dashboards,
        'messages': messages,
        'error_messages': error_messages
    })
    return HttpResponse(template.render(context))

def render_dashboard(request, title):
    if (not request.user.is_authenticated()):
        return login_user(request)
    
    dash = Dashboard.objects.filter(title=title)
    if len(dash) == 0:
        return redirect(settings.BASE_URL + "/list/")
    
    dashPerms = Dashboard_Permission.objects.filter(dashboard_title=title, user=request.user.username)
    if len(dashPerms)==0:
        return redirect(settings.BASE_URL + "/list/")

    template = loader.get_template('dashboard.html')
    dashboard = get_document_or_404(Dashboard, pk=title)
    topic_names = TopicWindowFunctions.get_topic_windows(dashboard.title)
    user_permissions_list = Dashboard_Permission.objects.filter(dashboard_title=dashboard.title)
    list_of_usernames = []
    for user_obj in user_permissions_list:
        list_of_usernames.append(user_obj.user)
    matched_usernames = check_for_active_users(list_of_usernames)
    print("topic_names is " + str(topic_names))
    context = RequestContext(request, {
        'dashboard': dashboard,
        'topic_names': topic_names,
        'connected_users': matched_usernames
    })
    return HttpResponse(template.render(context))

def dashboard_user_administration(request):
    messages = []
    error_messages = []
    postsbymonth = []
    topic_titles = []
    user_permissions_list = None
    request_type = "useraddtable"
    topicposts = []
    
    if (not request.user.is_authenticated()):
        return redirect(settings.BASE_URL)
    
    request_user = request.user.username


    # get dashboard title
    if  request.method == "POST":
        dash_title = request.POST['dashboard']
    else:
        dash_title = request.GET.get("dashboard")
    
        
    # retrieve dashboard and verify that the user has admin permissions
    dashboard = Dashboard.objects.get(title=dash_title)
    user_perm_level = None
    try:
        if request.user.is_superuser:
            user_perm_level = Dashboard_Permissions.ADMIN
        else:    
            user_perm = Dashboard_Permission.objects.get(dashboard_title=dash_title, user=request_user)
            user_perm_level = user_perm.privilege
    except:
        print "User," + request_user + " , does not have permissions for the " + dash_title + " Dashboard."
    print(user_perm_level)
    if user_perm_level != None:
        user_permissions_list = Dashboard_Permission.objects.filter(dashboard_title=dash_title)
        topic_titles = Topic.objects.filter(dashboard_title=dash_title, topic_active=True)
        
        if  request.method == "POST":            
            dash_action = request.POST['dashboard_action']
            request_type = request.POST['actionType']
            
            #implement for all users with access
            if dash_action=="add_user":
                action_user = request.POST['action_user']
                
                user_permission = request.POST["user_permission"]
                print user_permission
                success = add_dashboard_user(dash_title, action_user, user_permission)
                if (success):
                    messages.append("Successfully added the user: " + action_user)
                else:
                    error_messages.append("Unable to add user")
            elif dash_action=="add_topic":
                topic_name = request.POST['topic']
                
                successfull = TopicWindowFunctions.add_topic_window(topic_name,
                                                                    dash_title)
                if successfull:
                    messages.append("Successfully added topic " + topic_name)
                else:
                    error_messages.append("Failed to add topic.")
                
            
            elif dash_action == "deactivate_topic":
                topic_names = request.POST.getlist("checkedtopics")
                successfull = True
    
                for topic_name in topic_names:
                    if not TopicWindowFunctions.deactivate_topic_window(topic_name,
                                                                        dash_title):
                        successfull = False
                #topic_name = request.POST['topic']
                #successfull = deactivate_topic_window(topic_name, dash_title)
                if successfull:
                    messages.append("Successfully removed topics" )
                else:
                    error_messages.append("Failed to remove topic.")

            
            #implement for admin users
            elif (user_perm_level == Dashboard_Permissions.ADMIN ):
                print (request.POST['dashboard_action'])
                if request.POST['dashboard_action'] =="printmetricsreport":
                    return print_metrics(request)#redirect(settings.BASE_URL + "PrintMetrics/", request)
                
                if request.POST['dashboard_action']== "viewmetricsreport":
                    metricStartDate = request.POST["metricStartDate"]
                    metricEndDate = request.POST["metricEndDate"]
                    postsbymonth = retrieve_dashboard_posts_by_month(dash_title, metricStartDate, metricEndDate)
                    topicposts = retrieve_topic_window_posts(dash_title, metricStartDate, metricEndDate)
                else:
                    action_user = request.POST['action_user']
                    if action_user == dashboard.creator:
                        error_messages.append("Unable to perform Dashboard user action on Dashboard creator.")
                    else:
                        if dash_action == "delete_user":
                            success = delete_dashboard_user(dash_title, action_user)
                            if (success):
                                messages.append("Successfully deleted the user: " + action_user)
                            else:
                                error_messages.append("Unable to delete user")
                        elif dash_action == "change_permissions":
                            user_permission = request.POST["user_permission"]
                            success = change_dashboard_permissions(dash_title, action_user, user_permission)
                            if (success):
                                messages.append("Successfully change the user permissions." + action_user)
                            else:
                                error_messages.append("Unable to change user permissions.")
                        else:
                            error_messages.append("Invalid Dashboard User Action.")


                            
    print(messages)
    template = loader.get_template('dashboarduseractions.html')
    context = RequestContext(request, {
        'dashboard': dashboard,
        'user_permissions': user_permissions_list,
        'user_perm_level': user_perm_level,
        'request_type': request_type,
        'show_messages': messages,
        'error_messages': error_messages,
        'postsbymonth':postsbymonth,
        'topicposts':topicposts,
        'topictitles':topic_titles
    })
    return HttpResponse(template.render(context))

def print_metrics(request):
    postsbymonth = []
    topic_titles = []
    user_permissions_list = None
    request_type = "useraddtable"
    topicposts = []

    if (not request.user.is_authenticated()):
        return redirect(settings.BASE_URL)

    request_user = request.user.username


    # get dashboard title
    if  request.method <> "POST":
        redirect(settings.BASE_URL)

    dash_title = request.POST['dashboard']

    # retrieve dashboard and verify that the user has admin permissions
    dashboard = Dashboard.objects.get(title=dash_title)
    user_perm_level = None
    try:
        if request.user.is_superuser:
            user_perm_level = Dashboard_Permissions.ADMIN
        else:
            user_perm = Dashboard_Permission.objects.get(dashboard_title=dash_title, user=request_user)
            user_perm_level = user_perm.privilege
    except:
        print "User," + request_user + " , does not have permissions for the " + dash_title + " Dashboard."

    if user_perm_level ==  Dashboard_Permissions.ADMIN and request.method == "POST":
        metricStartDate = request.POST["metricStartDate"]
        metricEndDate = request.POST["metricEndDate"]
        postsbymonth = retrieve_dashboard_posts_by_month(dash_title, metricStartDate, metricEndDate)
        topicposts = retrieve_topic_window_posts(dash_title, metricStartDate, metricEndDate)


    template = loader.get_template('printdashboardmetrics.html')
    context = RequestContext(request, {
        'dashboard': dash_title,
        'user_permissions': user_permissions_list,
        'user_perm_level': user_perm_level,
        'request_type': request_type,
        'postsbymonth':postsbymonth,
        'topicposts':topicposts,
        'topictitles':topic_titles
    })
    return HttpResponse(template.render(context))

def send_message(request):
    """Stub for send message test case"""
    return None

def register(request):
    if request.method == "POST":
        user = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        messages = []
        statuscode = 200

        for user_obj in User.objects:
            if user_obj.username == user:
                messages.append("Username already exists")
                statuscode = 400
        if not RegistrationFunctions.validate_email(email):
            messages.append("Invalid Email")
            statuscode = 400
        if not RegistrationFunctions.validate_password(password):
            messages.append("Invalid Password")
            statuscode = 400

        
        if statuscode == 200:
            sessionUser =  get_user_model().objects.create_user(username=user, password=password, email=email)
            sessionUser.save()
            
            template = loader.get_template('Authentication/confirmregistration.html')
        else:
            template = loader.get_template('Authentication/registration.html')
            
        context = RequestContext(request, {'all_messages': messages, 'username':user, 'email':email})
        return HttpResponse( content=template.render(context), status=statuscode)
    else:
        template = loader.get_template('Authentication/registration.html')
        context = RequestContext(request, {
        'all_messages': None,
        })
        return HttpResponse(template.render(context))

def homepage(request):
    print "Homepage"
    return login_user(request)

def login_user(request):
    print "Login user"
    if request.user.is_authenticated():
        return redirect('list/')
    if request.method == "POST" and not request.user.is_authenticated():#and not request.user.is_authenticated(): #TODO: add in check for if user currently has a logged in session
       #request.session.create()
        usernm = request.POST['username']
        password = request.POST['password']
        user = None
        messages = []
        error_messages = []
        statuscode = 400 # assume credentials are invalid
              
        try:
            foundUser = User.objects.get(username=usernm)
            user = authenticate(username=usernm, password=password)
        except:
            pass #pass becuase error message will be added below
            

        if user is not None:
            # the password verified for the user
            if user.check_password(password):
                    statuscode = 200
                    login(request, user)

                    messages.append("User is valid, active and authenticated")
                    return redirect('list/')
            else:
                    error_messages.append("Invalid Username/Password combination.")
        else:   
            # the authentication system was unable to verify the username and password
            error_messages.append("Invalid Username/Password combination.")        
        
        if statuscode == 200:
            context = RequestContext(request, {'messages': messages, 'authenticated': True, 'error_messages':error_messages})
        else:
            context = RequestContext(request, {'messages': messages,'authenticated': False , 'error_messages':error_messages})            
        
        template = loader.get_template('Authentication/login.html')
        return HttpResponse( content=template.render(context), status=statuscode)
    else:
       template = loader.get_template('Authentication/login.html')
       context = RequestContext(request, {'messages': None, 'authenticated': False, 'error_messages':None} )        
    return HttpResponse(template.render(context))

def logoff_user(request):
    logout(request)
    request.session.delete()
    template = loader.get_template('Authentication/logoff.html')
    context = RequestContext(request, {'messages': None, 'authenticated': False} )  
    return HttpResponse(template.render(context))



#from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
def admin_functions(request):
    usernames = []
    dashboards = []
    userids = []
    dashprivfound = []
    
    if (not request.user.is_superuser):
        #remove before production... add setadminuser as parameter and use username as value
        if request.method=="GET" and request.GET.get("setadminuser") is not None:
            set_site_admin(request.GET.get("setadminuser"))
            
        #template = loader.get_template('Authentication/Login.html')
        #context = RequestContext(request, {}) 
        return redirect(settings.BASE_URL)#HttpResponse(template.render(context))
    actionselected = "user"
    
    if request.method=="POST" and request.POST['adminaction']== "delete":
        rmvuser = request.POST['username']
        delete_user(rmvuser)
        usernames = retrieve_all_usernames()
    
    elif request.method=="POST" and request.POST['adminaction']== "viewactiveusers":
        usernames = retrieve_active_usernames()
    
    elif request.method=="POST" and request.POST['adminaction']== "viewusers":
        usernames = retrieve_all_usernames()
        
    elif request.method=="POST" and request.POST['adminaction'] == "viewsiteadmins":
        usernames = view_site_admins()
        
    elif request.method=="POST" and request.POST['adminaction'] == "setadmin":
        set_site_admin(request.POST['username'])
        usernames = view_site_admins()
        
    elif request.method=="POST" and request.POST['adminaction'] == "removeadmin":
        remove_site_admin(request.POST['username'])
        usernames = view_site_admins()
    elif request.method=="POST" and request.POST['adminaction'] == "viewalldashboards":
        actionselected = "dashboard"
        dash_objs = Dashboard.objects()
        for dash in dash_objs:
            dashboards.append(dash.title)
        print(dashboards)
    elif request.method=="POST" and request.POST['adminaction'] == "deletedashboard":
        actionselected = "dashboard"
        delete_dashboard(request.POST['dashboard'])
        dash_objs = Dashboard.objects()
        for dash in dash_objs:
            dashboards.append(dash.title)
    elif request.method=="POST" and request.POST['adminaction'] == "viewuserdashboards":
        actionselected = "dashboard"
        dashprivfound = Dashboard_Permission.objects.filter(user=request.POST['dashusername'])
    elif request.method=="POST":
        print(request.POST['adminaction'])
    
        
    print(actionselected)
    template = loader.get_template('Administration/adminfunctions.html')
    context = RequestContext(request, {'ursfound': usernames , 'dashboardsfound': dashboards, 'actionselected': actionselected, 'dashprivfound':dashprivfound }) 
    return HttpResponse(template.render(context))

def admin_dashboard_functions(request):
    dashboard = []
    userids = []
    
    if request.method=="POST" and request.POST['useraction']== "delete":
        rmvuser = request.POST['username']
        delete_user(rmvuser)        
        usernames = retrieve_all_usernames()
        
    elif request.method=="POST" and request.POST['useraction']== "viewactiveusers":
        usernames = retrieve_active_usernames()
        
    elif request.method=="POST" and request.POST['useraction']== "viewusers":
        usernames = retrieve_all_usernames()


        

    dashprivs = Dashboard_Permission.objects()
    template = loader.get_template('AdminDashboardFunctions.html')
    context = RequestContext(request, {'dashprivfound': dashprivs,})

    return HttpResponse(template.render(context))

def password_functions(request):
    form_type = ""
    screen_title = ""
    error_messages = []
    messages = []
    context = None
    # handle posts
    if request.method == "POST" : 
        #handle change password request       
        if request.POST['password_action'] == "Change Password" :
            screen_title = "Change Password"
            username = request.POST["username"]
            current_password = request.POST["current_password"]
            new_password = request.POST["password"]
            
            screen_title = "Change Password"
            
            if validate_password(new_password):
                if change_password(username, current_password, new_password):
                    form_type = "sucessfullchange"
                    messages.append("Password successfully changed.")
                    form_type = "successfullchange"
                else:
                    error_messages.append("Invalid username/password combination.")
                    form_type = "changepassword"
            else:
                form_type = "changepassword"
                error_messages.append("Invalid password format.")
                
            
        #handle reset email request
        elif request.POST['password_action'] == "Reset Password": 
            generate_reset_email(request.POST['username'])
            form_type = "checkemail"
            screen_title = "Reset Password"
            messages.append("Please check your email for a password reset link.")
                
        #handle reset request with pin and username from email
        elif request.POST['password_action'] == "Reset My Password":
            screen_title = "Reset Password"
            username = request.POST['username']
            pin = request.POST['pin']
            password = request.POST['password']
            reset_error_message = reset_password(username, pin, password)
            if reset_error_message == None:
                form_type="successfulchange"
                messages.append("Password successfully reset.")
            else:                
                form_type = "resetpassword"
                error_messages.append("Password Reset Failed")
                error_messages.append(reset_error_message)
                
        # all gets that do not match a valid form_action should error
        else:
            screen_title = "ERROR"
            error_messages.append("Please use the appropriate link.")
    # handle gets
    else:
        if request.GET.get("function") == "changepassword":
            screen_title = "Change Password"
            form_type = "changepassword"
            
        #handle initial resetpasword link request 
        elif request.GET.get("function") =="resetpassword":
            screen_title = "Reset Password"
            form_type = "resetpassword"
            
        #handle reset password request from email link
        elif request.GET.get("function") =="resetpinsuccessful":
            screen_title = "Reset Password"
            username = request.GET.get("username")
            pin = request.GET.get('pin')
            form_type = "resetpinsuccessful"
            context = RequestContext(request, {'screen_title':screen_title , 'messages':messages, 'error_messages':error_messages, 'form_type': form_type, 'reset_username':username, 'reset_pin':pin })
        
        # all gets that do not match a valid function should error
        else:
            screen_title = "ERROR"
            error_messages.append("Please use the appropriate link.")
    
    template = loader.get_template('Authentication/resetpassword.html')
    if context == None:
        context = RequestContext(request, {'screen_title':screen_title , 'messages':messages, 'error_messages':error_messages, 'form_type': form_type })
        
    return HttpResponse(template.render(context))
