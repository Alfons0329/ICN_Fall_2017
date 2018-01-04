#! /usr/bin/python

import time

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, Switch
from mininet.cli import CLI


class Router(Node):
    "Node with Linux Router Function"

    def config(self, **params):
        super(Router, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Router, self).terminate()


def topology():
    net = Mininet(autoStaticArp=True)

    # Initialize objects dicts
    hosts, switches, routers = {}, {}, {}

    # Create Host, from h1 to h6
    for i in range(6):
        host = net.addHost('h%d' % (i + 1))
        hosts['h%d' % (i + 1)] = host

    # Create Switch, from s1 to s5
    for i in range(5):
        switch = net.addSwitch('s%d' % (i + 1), failMode='standalone')
        switches['s%d' % (i + 1)] = switch

    # Create Router, from r1 to r4
    for i in range(4):
        router = net.addHost('r%d' % (i + 1), cls=Router)
        routers['r%d' % (i + 1)] = router

    links = [('s1', 'r1'), ('s1', 'r2'), ('s2', 'r1'), ('s2', 'r3'),
             ('s2', 'r4'), ('s3', 'r3'), ('s3', 'h1'), ('s3', 'h2'),
             ('s4', 'r4'), ('s4', 'h3'), ('s4', 'h4'), ('s5', 'r2'),
             ('s5', 'h5'), ('s5', 'h6')]

    for link in links:
        src, dst = link
        net.addLink(src, dst)

    net.start()

    # Configure network manually
    config(hosts, switches, routers)

    # Comment this line if you don't need to debug
    CLI(net)

    # Checking homework's status
    if check(hosts):
        print('\033[92mYou pass the Test, congs! you finished your homework!\033[0m')
    else:
        print('\033[91mHmm, looks some network configurations wrong in your code.\033[0m')

    net.stop()


def config(hosts, switches, routers):

    # Hosts, Routers IP configuration
    hosts['h1'].cmd('ifconfig h1-eth0 192.168.1.1/26')
    hosts['h2'].cmd('ifconfig h2-eth0 192.168.1.2/26')
    hosts['h3'].cmd('ifconfig h3-eth0 192.168.1.65/26')
    hosts['h4'].cmd('ifconfig h4-eth0 192.168.1.66/26')
    hosts['h5'].cmd('ifconfig h5-eth0 192.168.2.1/24')
    hosts['h6'].cmd('ifconfig h6-eth0 192.168.2.2/24')

    routers['r1'].cmd('ifconfig r1-eth0 put_your_config_here')
    routers['r1'].cmd('ifconfig r1-eth1 put_your_config_here')
    routers['r2'].cmd('ifconfig r2-eth0 put_your_config_here')
    routers['r2'].cmd('ifconfig r2-eth1 put_your_config_here')
    routers['r3'].cmd('ifconfig r3-eth0 10.0.1.2/24')
    routers['r3'].cmd('ifconfig r3-eth1 192.168.1.62/26')
    routers['r4'].cmd('ifconfig r4-eth0 10.0.1.3/24')
    routers['r4'].cmd('ifconfig r4-eth1 192.168.1.126/26')

    # Host routing table configuration
    hosts['h1'].cmd('route add default gw 192.168.1.62')
    hosts['h2'].cmd('put_your_config_here')
    hosts['h3'].cmd('put_your_config_here')
    hosts['h4'].cmd('put_your_config_here')
    hosts['h5'].cmd('put_your_config_here')
    hosts['h6'].cmd('put_your_config_here')

    # Router routing table configuration
    routers['r1'].cmd('put_your_config_here')
    routers['r1'].cmd('put_your_config_here')
    routers['r1'].cmd('put_your_config_here')
    routers['r2'].cmd('put_your_config_here')
    routers['r2'].cmd('put_your_config_here')
    routers['r3'].cmd('route add -net 192.168.1.64/26 gw 10.0.1.3')
    routers['r3'].cmd('put_your_config_here')
    routers['r4'].cmd('route add -net 192.168.1.0/26 gw 10.0.1.2')
    routers['r4'].cmd('put_your_config_here')


def check(hosts):
    ips = {'h1': '192.168.1.1', 'h2': '192.168.1.2',
           'h3': '192.168.1.65', 'h4': '192.168.1.66',
           'h5': '192.168.2.1', 'h6': '192.168.2.2'}

    for pair in [(src, dst) for src in ips for dst in ips if src != dst]:
        src, dst = pair
        checkstr = hosts[src].cmd('ping %s -c 1 -W 1' % ips[dst])
        if '64 bytes from %s' % ips[dst] not in checkstr:
            print('\033[93m%s can\'t connect to %s\033[0m' % (src, dst))
            return False

    return True

if __name__ == '__main__':
    topology()
