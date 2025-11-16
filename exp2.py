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
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(s1, s2)
        self.addLink(s2, h3)

def main():
    print("Creating network...")
    net = LinearTopo()
    setLogLevel('info')
    net = Mininet(topo = net, 
                switch = OVSKernelSwitch, 
                controller = DefaultController,
                autoSetMacs = True
                )
    net.start()
    h1 = net.get('h1').cmd('/usr/sbin/sshd')
    h2 = net.get('h2').cmd('/usr/sbin/sshd')
    h3 = net.get('h3').cmd('/usr/sbin/sshd')

    with open('result2.txt', 'w') as f:
        f.write('=== Initial ===\n')
        f.write('h1 -> h3\n' + h1.cmd('ping -c 1 h3') + '\n')
        f.write('h2 -> h3\n' + h2.cmd('ping -c 1 h3') + '\n')
        f.write('Instructions:\n')
        f.write('Run these in another terminal:\n')
        f.write('  sudo ovs-ofctl show s1\n')
        f.write('  sudo ovs-ofctl dump-flows s1\n')
        f.write('  sudo ovs-ofctl add-flow s1 "in_port=2,actions=drop"\n')
        f.write('  sudo ovs-ofctl add-flow s1 "in_port=1,actions=output:3"\n')

    info('Now open another terminal and issue ovs-ofctl commands on s1.\n')
    info('After adding flows, come back and run the verification below.\n')

    CLI(net)
    net.stop()



if __name__ == '__main__':
    main()  
