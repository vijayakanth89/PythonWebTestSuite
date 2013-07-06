from twisted.internet import reactor
from twisted.web.static import File
from twisted.internet import task
from websocket import WebSocketSite, WebSocketHandler
from threading import Thread

import random


class TickerHandler(WebSocketHandler):
    def __init__(self, transport):
        WebSocketHandler.__init__(self, transport)
        self.task = None

    def __del__(self):
        print 'Deleting Handler'

    def send_time(self, symbol):
        data = random.randint(0, 12345);
        print data
        print symbol
        self.transport.write(symbol + ":" + str(data))

    def frameReceived(self, frame):
        print "Peer: ", self.transport.getPeer()
        print frame 
        if self.task != None:
            self.task.stop()
            
        self.task = task.LoopingCall(self.send_time, (frame))
        self.task.start(0.5)


    def connectionMade(self):
        print 'Connected to client.'
          

    def connectionLost(self, reason):
        print 'Lost connection.'
        if self.task != None:
            self.task.stop()
        # here is a good place to deregister this handler object


class Ticker(Thread):
    def __init__(self, port=9090):
        Thread.__init__(self)
        self.port = port
        
    def run(self):
        root = File('.')
        site = WebSocketSite(root)
        site.addHandler('/test', TickerHandler)
        print "\nWebSocket Server starts at %d" % self.port
        reactor.listenTCP(self.port, site)
        reactor.run(installSignalHandlers=0)

    def stop(self):
        print "Shutting down WebSocket Server\n"
        reactor.stop()


if __name__ == "__main__":
    # run our websocket server
    # serve index.html from the local directory
    root = File('.')
    site = WebSocketSite(root)
    site.addHandler('/test', TickerHandler)
    reactor.listenTCP(9090, site)
    reactor.run()
