from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


"""linear topology example:

   h1----s1---s2----h3  
         |              
         h2

"""
class LinearTopo(Topo):
    def __init__(self):
        super().__init__()

        # Define hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Define links between nodes
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h3)

def main():
    info("Creating network...")
    net = LinearTopo()
    setLogLevel('info')

    # Create the Mininet instance with the defined topology, switches, and controller
    net = Mininet(topo = net, 
                switch = OVSKernelSwitch, 
                controller = DefaultController,
                autoSetMacs = True
                )
    net.start()
    info('Network created.\n')

    #sudo ovs-ofctl add-flow s1 "in_port=2,actions=drop"
    #sudo ovs-ofctl add-flow s1 "in_port=1,actions=output:3"

    info('Open another terminal and add ovs-ofctl add-flows commands on s1.\n')
    info(' After set up the flows, start testing with connectivity.\n')
    CLI(net)
    net.stop()



if __name__ == '__main__':
    main()  
