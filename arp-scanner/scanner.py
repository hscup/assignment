#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import os
import sys

import nmap
from python_arptable import get_arp_table


class ArpScanner(object):
    """
    ARP scanner
    """
    def __init__(self):
        self.arp_hosts = []
        try:
            self.nm = nmap.PortScanner()
        except nmap.PortScannerError:
            print('Nmap not found, please install nmap first', sys.exc_info()[0], file=sys.stderr)
            sys.exit(1)
        except:
            print("Unexpected error:", sys.exc_info()[0], file=sys.stderr)
            sys.exit(1)
    
    def get_arp_hosts(self):
        """
        Return list of arp hosts from arp cache
        """
        for arp in get_arp_table():
            if arp.get('IP address'):
                self.arp_hosts.append(arp.get('IP address'))

    
    def scan(self, host=None, udp_port_ranges=None, tcp_port_ranges=None):
        if host:
            # Clear the list of arp cache, just scan the given host
            self.arp_hosts[:] = []
            self.arp_hosts.append(host)
        else:
            self.get_arp_hosts()

        ports = ''
        if udp_port_ranges:
            ports += 'U:' + udp_port_ranges
        if tcp_port_ranges:
            # Add comma to seperate udp and tcp ports
            ports += ',' if ports else ''
            # Add tcp port ranges
            ports += 'T:' + tcp_port_ranges
        
        if not ports:
            ports = None

        for arp_host in self.arp_hosts:
            try:
                # Scan the host with OS detection option
                scan_result = self.nm.scan(hosts=arp_host, ports=ports, arguments='-O')
                # Check if host being scanned is up or down
                is_uphost = False
                if 'scan' in scan_result:
                    is_uphost = scan_result['scan']
                if not is_uphost:
                    continue

                # Get open TCP/UDP ports
                tcp_ports = ','.join([str(i) for i in self.nm[arp_host].all_tcp()])
                udp_ports = ','.join([str(i) for i in self.nm[arp_host].all_udp()])
                os_type = ''
                # The nmap command return guess list of devices
                # We chose the os with highest accuracy
                if 'osmatch' in self.nm[arp_host]:
                    accuracy = -1
                    for os_match in self.nm[arp_host]['osmatch']:
                        if int(os_match['accuracy']) > accuracy:
                            accuracy = int(os_match['accuracy'])
                            os_type = os_match['name']
                
                if 'osclass' in self.nm[arp_host]:
                    accuracy = -1
                    for os_class in self.nm[arp_host]['osclass']:
                        if int(os_class['accuracy']) > accuracy:
                            accuracy = int(os_class['accuracy'])
                            os_type = os_class['type']

                # print to console as TSV format
                print('{0}\t{1}\t{2}\t{3}'.format(arp_host, tcp_ports, udp_ports, os_type))
            except nmap.PortScannerError:
                # ignore current host, continue scan other
                pass
            except Exception as ex:
                print(ex)
                print("Unexpected error:", sys.exc_info()[0], file=sys.stderr)
                sys.exit(0)


def main():
    # Add options for command line running
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--host', help='host to scan')
    parser.add_argument('-t', '--tcp', help='TCP port ranges, <start_port>-<end_port>')
    parser.add_argument('-u', '--udp', help='UDP port ranges, <start_port>-<end_port>')
    args = parser.parse_args()

    print('host\topen_tcp_ports\topen_udp_ports\tos_type')
    host = args.host
    udp_port_ranges = args.udp
    tcp_port_ranges = args.tcp
    scanner = ArpScanner()
    scanner.scan(host, udp_port_ranges, tcp_port_ranges)


if __name__ == '__main__':
    # check if current user is root
    if os.getuid() != 0:
        print("This program must be run as root. Exiting...", file=sys.stderr)
        sys.exit(1)

    main()
