from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted_websockets import WebSocketsResource, lookupProtocolForFactory

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
        print "Disconnected for reason: " + str(reason) + "\nConnected clients: " + str(self.factory.clients)

    def dataReceived(self, data):
        print "Received data: " + str(data)
        for c in self.factory.clients:
            c.sendLine("<{}> {}".format(self.transport.getHost(), data))



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

