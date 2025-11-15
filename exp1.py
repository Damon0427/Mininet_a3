from mininet.net import Mininet 
from mininet.node import Node, OVSKernelSwitch, Controller, RemoteController 
from mininet.cli import CLI 
from mininet.link import TCLink 
from mininet.topo import Topo 
from mininet.log import setLogLevel, info 
import argparse


# allowing the node to act as a router, and forward packets between its interfaces
class Router( Node ):
    def config( self, **params ):
        super( Router, self ).config( **params )
        # Enable IP forwarding
        info('enabling IP forwarding on router\n',self)
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( Router, self ).terminate()


def ip(subnet,host,prefix=None):

    addr = '10.0.'+str(subnet)+'.' + str(host)
    if prefix != None: addr = addr + '/' + str(prefix)
    return addr