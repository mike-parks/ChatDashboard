__author__ = 'Nick'
from chatapp.models import Topic


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