from twisted.internet import reactor, protocol
from twisted.protocols import basic

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

reactor.listenTCP(1025, DashboardProtocolFactory())
reactor.run()

