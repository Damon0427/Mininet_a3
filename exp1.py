from mininet.net import Mininet 
from mininet.cli import CLI 
from mininet.link import TCLink 
from mininet.topo import Topo 
from mininet.node import Node
from mininet.log import  info 
from mininet.log import setLogLevel
import argparse



# allowing the node to act as a router, and forward packets between its interfaces
class Router( Node ):
    def config( self, **params ):
        super( Router, self ).config( **params )
        # Enable IP forwarding
        info('enabling IP forwarding on router',self, '\n')
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( Router, self ).terminate()

"""
    topology:

    h1---r1---r2---h3
          |
          h2    
    
"""

class RTopo(Topo):
    def __init__(self):
        super().__init__()
        h1 = self.addHost('h1', ip=ip(0,1,24), defaultRoute='via '+ip(0,3))  
        h2 = self.addHost('h2', ip=ip(3,2,24), defaultRoute='via '+ip(3,4))  
        h3 = self.addHost('h3', ip=ip(2,2,24), defaultRoute='via '+ip(2,1))  
        r1 = self.addHost('r1', cls=Router)
        r2 = self.addHost('r2', cls=Router)
        self.addLink(h1, r1, intfName1='h1-eth0', intfName2='r1-eth0')   
        self.addLink(r1, r2, intfName1='r1-eth1', intfName2='r2-eth0')   
        self.addLink(r2, h3, intfName1='r2-eth1', intfName2='h3-eth0')   
        self.addLink(r1, h2, intfName1='r1-eth2', intfName2='h2-eth0')  

def staticRouting(r1, r2):
    r1.cmd('ip route add 10.0.2.0/24 via 10.0.1.2 dev r1-eth1')
    r2.cmd('ip route add 10.0.0.0/24 via 10.0.1.1 dev r2-eth0')
    r2.cmd('ip route add 10.0.3.0/24 via 10.0.1.1 dev r2-eth0')


def ip(subnet,host,prefix=None):
    addr = '10.0.'+str(subnet)+'.' + str(host)
    if prefix != None: addr = addr + '/' + str(prefix)
    return addr

def main():
    setLogLevel('info')
    topo = RTopo()
    net = Mininet(topo=topo, link=TCLink, autoSetMacs = True)
    net.start()
    r1, r2 = net.get('r1'), net.get('r2')

    r1.cmd('ifconfig r1-eth0 ' + ip(0,3,24))
    r1.cmd('ifconfig r1-eth1 ' + ip(1,1,24))
    r1.cmd('ifconfig r1-eth2 ' + ip(3,4,24))
    r2.cmd('ifconfig r2-eth0 ' + ip(1,2,24))
    r2.cmd('ifconfig r2-eth1 ' + ip(2,1,24))
    staticRouting(r1, r2)
    h1, h2, h3 = net['h1'], net['h2'], net['h3']
    with open('result1.txt', 'w') as f:
        f.write('h1 -> h3\n' + h1.cmd('ping -c 1 10.0.2.2') + '\n')
        f.write('h2 -> h3\n' + h2.cmd('ping -c 1 10.0.2.2') + '\n')
        f.write('h3 -> h1\n' + h3.cmd('ping -c 1 10.0.0.1') + '\n')
        f.write('h3 -> h2\n' + h3.cmd('ping -c 1 10.0.3.2') + '\n')

    CLI(net) 
    net.stop()

if __name__ == '__main__':
    main()


