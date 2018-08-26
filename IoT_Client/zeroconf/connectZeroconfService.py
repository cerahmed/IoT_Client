import socket
from socket import inet_ntoa
from zeroconf import ServiceBrowser, Zeroconf
import requests

# flag to hold service connectivity
connected = False

def myLocalIP():
    
    # retrieve hostname from socket
    hostname = socket.gethostname()
    
    # find local ipaddress to for other devices to connect to
    # and to use it in advertising zeroconf service
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = s.getsockname()[0]
    
    # for debugging purposes
    print("Hostname: {}".format(hostname))
    print("IP Address: {}".format(IPAddr))
    
    # close socket connection
    s.close()
    
    # return both hostname and local IP Address
    return hostname, IPAddr

class MyListener(object):

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        hostname = info.server
        hostname = hostname.replace('.local.', '')
        ipaddress = inet_ntoa(info.address)
        port = info.port
        
        # call the server handling function
        self.handleServer(name, hostname, ipaddress, port)

    def handleServer(self, servicename, hostname, ipaddress, port):
        global connected
        if connected:
            return
        
        # for debugging purposes
        print("Handling: {}".format(servicename))
        
        # string for full server registration url
        registrationURL = 'http://{}:{}/devices/register'.format(ipaddress,
                                                                 port)
                          
        # try to reach out -> if successful: change connected to True 
        try:
            r = requests.get(registrationURL)
            if r.status_code == 200:
                connected = True
                print("Connected successfully to {}".format(servicename))
            
        except:
            print("Could not connect to {}".format(servicename))
        
def connectToServer():
    global connected
    
    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_IoT-server._tcp.local.", listener)
    
    while not connected:
        pass