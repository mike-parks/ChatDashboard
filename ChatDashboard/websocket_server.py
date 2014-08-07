from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted_websockets import WebSocketsResource, lookupProtocolForFactory
from chatapp.models import Message
from TopicWindowFunctions import add_topic_window, deactivate_topic_window
from chatapp.models import Topic
import datetime

DBNAME = "chatdata"
import mongoengine
mongoengine.connect(DBNAME)

"""Creating Twisted protocol class.
Requires these functions: connectionMade, connectionLost, lineReceived."""
class DashboardProtocol(basic.LineReceiver):

    def __init__(self, factory):
        self.setLineMode()
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)
        print "Connected. Connected clients: " + str(self.factory.clients)
        #for c in self.factory.clients:
        #    c.sendLine("<{}> {}".format(self.transport.getHost(),
        #               "Test message"))

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print "Disconnected for reason: " + str(reason) + \
              "\nConnected clients: " + str(self.factory.clients)

    def dataReceived(self, data):
        print "Received data: " + str(data)

        topic_window_split = str(data).split(":-:")
        if len(topic_window_split) > 1:
            dashboardname = topic_window_split[0]
            topicname = topic_window_split[1]
            action = topic_window_split[2]
            if action == "add":
                add_topic_window(topicname, dashboardname)
            elif action == "delete":
                deactivate_topic_window(topicname, dashboardname)
            for c in self.factory.clients:
                messageFormatted = "<{}> {}".format(self.transport.getHost(), dashboardname
                                            + ":-:" + topicname + ":-:" + action)
                c.sendLine(messageFormatted)
            return

        topic_window_split = str(data).split(":--:")
        if len(topic_window_split) > 1:
            dashboardname = topic_window_split[0]
            username = topic_window_split[1]
            action = topic_window_split[2]
            for c in self.factory.clients:
                messageFormatted = "<{}> {}".format(self.transport.getHost(), dashboardname
                                            + ":--:" + username + ":--:" + action)
                c.sendLine(messageFormatted)
            return

        # construct a model object message
        splitinfo = str(data).split("::",3)
        username = splitinfo[2]
        messagetext = splitinfo[3]
        topicname = splitinfo[1]
        dashboardname = splitinfo[0]
        message = Message(msgtext=messagetext,
                          timestamp=datetime.datetime.now(),
                          username=username,
                          dashboardtitle=dashboardname,
                          topic=topicname)
        message.save()


        #to_save_topic = True
        #for topic_window in Topic.objects:
        #    if topic_window.topic_title == topicname:
        #        to_save_topic = False

        #if to_save_topic:
        #    topic = Topic(topic_title = topicname,
        #                  topic_active = True,
        #                  dashboard_title = dashboardname)
        #    topic.save()

        for c in self.factory.clients:
            messageFormatted = "<{}> {}".format(self.transport.getHost(), dashboardname
                                        + "::" + topicname + "::" + username +
                                        "::" + messagetext)
            print "Message formatted is:" + messageFormatted
            c.sendLine(messageFormatted)

"""Factory for DashboardProtocol class.
Each instance will store its own unique set of connected clients."""
class DashboardProtocolFactory(protocol.Factory):

    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return DashboardProtocol(self)


found_protocol = lookupProtocolForFactory(DashboardProtocolFactory())
resource = WebSocketsResource(found_protocol)
root = Resource()
root.putChild("ws", resource)
reactor.listenTCP(1025, Site(root))
print("Running WebSocket server on ws://127.0.0.1:1025/ws")
reactor.run()


