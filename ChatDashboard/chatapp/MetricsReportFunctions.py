__author__ = 'Dave'
from models import Message
import datetime
import calendar
from django.db.models import Count

def get_date_from_unicode(udate, startday):
    udate.encode('ascii','ignore')

    month = int(udate[5:7])
    year = int(udate[0:4])
    if startday == "Beginning":
        day = 1
    elif startday == "End":
        monthlastday = calendar.monthrange(year, month)
        day = monthlastday[1]
    else:
        day = int(udate[8:10])


    date = datetime.datetime(year=year,month=month, day=day)

    return date

def retrieve_dashboard_posts_by_month(dashboard, start, end):
    month_metrics = []

    tempdate = get_date_from_unicode(start, "Beginning")
    enddate = get_date_from_unicode(end, "End")

    monthlastday = calendar.monthrange(tempdate.year, tempdate.month)
    previous_month = tempdate - datetime.timedelta(days=monthlastday[1])
    monthlastday = calendar.monthrange(previous_month.year, previous_month.month)
    previous_month = previous_month.replace(day=monthlastday[1])

    while tempdate.year <= enddate.year and tempdate.month <= enddate.month:
        previous_month = tempdate

        monthlastday = calendar.monthrange(previous_month.year, previous_month.month)
        tempdate = tempdate + datetime.timedelta(days=monthlastday[1])


        posts = Message.objects.filter(dashboardtitle = dashboard, timestamp__gt = previous_month, timestamp__lt = tempdate)

        temp_metric = dashboard_posts_metric()
        temp_metric.month = previous_month.strftime("%B %Y")
        temp_metric.num_posts = len(posts)
        month_metrics.append(temp_metric)

    return month_metrics

def retrieve_topic_window_posts(dashboard, start, end):
    month_metrics = []
    startdate = get_date_from_unicode(start, "Normal")
    enddate = get_date_from_unicode(end, "Normal")

    topicnames = Message.objects.filter(dashboardtitle = dashboard, timestamp__gt = startdate, timestamp__lt = enddate)#.item_frequencies('topic')

    #print(topicnames)

    temp_messages = []
    for message in topicnames:
        addmessagetotopic(message, temp_messages)



    for topic in topicnames:
        print(topic)
        topictitle = topic.title
        print(topictitle)

        tempposts = dashboard_posts_metric()
        #messagecounts = Message.objects.filter(dashboardtitle = dashboard, timestamp__gt = startdate, timestamp__lt = enddate).item_frequencies('username')
        messagecounts = Message.objects.filter(dashboardtitle = dashboard, timestamp__gt = startdate, timestamp__lt = enddate, topic = topictitle).item_frequencies('username')
        for messagecount in messagecounts:
            myuserpost = userpost()
            myuserpost.userid = messagecount.username
            #myuserpost.ucount =


        month_metrics.append(tempposts)

    #messagecounts = Message.objects.filter(dashboardtitle = dashboard, timestamp__gt = startdate, timestamp__lt = enddate).item_frequencies('username')
    #counts = Message.objects.values('username').annotate(dcount=Count('username'))
    print(messagecounts)
    temp_metric = dashboard_posts_metric()

    month_metrics.append( temp_metric)

    return month_metrics

def addmessagetotopic(message, messagecounts):
    found_topic = False
    for dashpost in messagecounts:
        if dashpost.topic == message.topic:
            addmesagecounttouser(message.username, dashpost.userposts)
            found_topic = True
            break

    if not found_topic:
        temp_post = dashboard_posts_metric()
        temp_post.topic = message.topic

        temp_user = userpost()
        temp_user.userid = message.username
        temp_user.numposts = 1

        temp_post.userposts.append(temp_user)

        messagecounts.append(temp_post)




def addmesagecounttouser(username, userposts):
    founduser = False
    for userpost in userposts:
        if userpost.userid == username:
            userpost.numposts = userpost.numposts + 1
            break

    if not founduser:
        temp_userpost = userpost()
        temp_userpost.userid = username
        temp_userpost.numposts = 1
        userposts.append(temp_userpost)



class dashboard_posts_metric():
    topic = ""
    userposts = []

class userpost():
    userid = ""
    numposts = 0

class dashboard_posts_metric():
    month =  None
    num_posts = 0
