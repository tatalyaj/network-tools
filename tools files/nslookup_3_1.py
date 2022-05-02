# Author: Talya Shaltiel ID: 207316670
# This is an implementation of the command nslookup using scapy
from scapy.all import *
import sys
i, o, e = sys.stdin, sys.stdout, sys.stderr
sys.stdin, sys.stdout, sys.stderr = i, o, e
PTR_CMND = "-type=PTR"
LOCAL_SERVER = "netbox."  # My local server (ISP)


def print_ip_address(dns_packet):

    count = dns_packet[DNS].ancount
    if count == 1:
        # If there's only a single answer
        if dns_packet[DNSRR].type == 1:
            # Type A
            print("Name: " + dns_packet[DNSRR].rrname.decode())
            print("Address: ")
            print("             " + dns_packet[DNSRR].rdata)
        elif dns_packet[DNSRR].type == 5:
            # Type CNAME
            print("Aliases: ")
            print("             " + dns_packet[DNSRR].rrname.decode())
    else:
        for j in range(count):
            if dns_packet[DNSRR][j].type == 1:
                # if  DNS resource record in the packet and type is A(# of A is 1)
                name = dns_packet[DNSRR][j].rrname.decode()
                name_without_dot = name[:-1]
                print("Name: " + name_without_dot)
                print("Addresses: ")
                print("             " + dns_packet[DNSRR][j].rdata)
        for k in range(count):
            if dns_packet[DNSRR][k].type == 5:
                # Type CNAME
                print("Aliases: ")
                aliases = dns_packet[DNSRR][k].rrname.decode()
                aliases_without_dot = aliases[:-1]
                print("             " + aliases_without_dot)


def print_domain_name(dns_packet):
    # If its type PTR
    if dns_packet[DNS].an is None:
        print("*** " + LOCAL_SERVER + " Can't find " + dns_packet[DNSQR].qname.decode() + ": Non-existent domain")
    else:
        count = dns_packet[DNS].ancount
        for j in range(count):
            if dns_packet[DNSRR][j].type == 12:
            # IN ORDER TO SEE THAT WRITE: python nslookup_1.py -type=PTR 8.8.8.8
                if dns_packet[DNSQR].qname == dns_packet[DNS].an[DNSRR].rrname:
                    name = dns_packet[DNS].an[DNSRR].rdata.decode()
                    name_without_dot = name[:-1]
                    print(dns_packet[DNS].an[DNSRR].rrname.decode() + "   name = " + name_without_dot)


def main(cmd):
    # path1 = 1
    # _action = sys.argv[path1]
    _action = cmd.split(" ")
    # if _action == PTR_CMND:
    if _action[0] == PTR_CMND:
        # path2 = 2
        # _ip_address = sys.argv[path2]  # The ip ex: 10.100.102.23
        _ip_address = _action[1]  # The ip ex: 10.100.102.23
        _ip_address_list = _ip_address.split(".")  # ex: ['10', '100', '102', '23']
        _ip_address_list_reverse = _ip_address_list[::-1]  # ex:['23', '102', '100', '10']
        _ip_reverse = ".".join(_ip_address_list_reverse)  # ex:23.102.100.10
        # Reversed 'cause that's the answer form
        _qname = _ip_reverse + ".in-addr.arpa"
        # Creating the DNS querry packet
        dns_packet = IP(dst="8.8.8.8") / UDP(sport=24601, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(qtype=12, qname=_qname)
        response_packet = sr1(dns_packet, timeout=5, verbose=False)  # Getting the packet that concerns us
        print_domain_name(response_packet)    # type PTR
    elif _action[0].endswith(".com"):  # if that's the "www.example.com" form then its the A type actions...
        # If _action != PTR_CMND then it means we have only one argument, otherwise we have 2
        _qname = _action[0]  # The name on which we question  the servers
        # Creating the DNS querry packet
        dns_packet = IP(dst="8.8.8.8") / UDP(sport=24601, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(qname=_qname)
        response_packet = sr1(dns_packet, timeout=5, verbose=False)  # Getting the packet that concerns us
        print_ip_address(response_packet) # type A, CNAME
    else:
        print("ERROR")


if __name__ == "__main__":
    main()