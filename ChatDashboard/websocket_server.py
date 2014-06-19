from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted_websockets import WebSocketsResource, lookupProtocolForFactory

"""Creating Twisted protocol class.
Requires these functions: connectionMade, connectionLost, lineReceived."""
class DashboardProtocol(basic.LineReceiver):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        for c in self.factory.clients:
            c.sendLine("<{}> {}".format(self.transport.getHost(), line))

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
reactor.run()


