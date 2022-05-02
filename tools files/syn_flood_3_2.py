# Author: Talya Shaltiel
# In this exercise we were given a pcap package and were asked to monitor the suspicious IP addresses
# Keeping in mind the SynFlood DoS attack
from scapy.all import *
import sys
i, o, e = sys.stdin, sys.stdout, sys.stderr
sys.stdin, sys.stdout, sys.stderr = i, o, e
#               *****   PATHS! *****
SYN_FLOOD_SAMPLE_PATH = r"C:/Users/tatal/OneDrive/Documents/College/Networks_class/syn_flood/SynFloodSample.pcap"
ATTACKERS_FILE_PATH = r"C:/Networks/work/attackersListFiltered.txt"
#                       ENDPATHS
attackersListFile = open(ATTACKERS_FILE_PATH, 'w')

# Flags hex values (got it from the pcap file)
SYN = 0x02
ACK = 0x10
SYN_ACK = 0x012
# Delta time value
delta_time = 0.000206  # Explained in the word file why i chose that num


def main():
    # Opens pcap file
    pcapFile = rdpcap(SYN_FLOOD_SAMPLE_PATH)
    print('opened')
    # Lists and dictionaries
    suspicious_ip_addresses_fast_syn_list = []
    suspicious_ip_addresses_no_ack_list = []
    suspicious_ip_addresses_list = []  # all the suspicious addresses
    syn_ip_time_packets_dict = {}
    ack_dict = {}
    # Condition checking- syn ack without ack
    for pkt in pcapFile:
        if TCP in pkt:
            if pkt[TCP].flags == ACK:
                # Checks the packet's TCP flag type is  ACK
                # If it is, the packet's IP destination and source addresses are added to the ack dictionary : ack_dict
                # When the IP source addresses is the key and the IP destination  addresses is the value.
                ack_dict[pkt[IP].src] = pkt[IP].dst
            elif pkt[TCP].flags == SYN_ACK:
                # Checks the packet's TCP flag type is SYN ACK
                if pkt[IP].dst in suspicious_ip_addresses_no_ack_list:
                    # Checks if it's  in suspicious ip's list: suspicious_ip_addresses_no_ack_list
                    # If so it continues to the next iteration, and does nothing.
                    continue
                elif pkt[IP].dst in ack_dict.keys():
                    # Checks if the IP destination  address  is  in the ack dictionary as key
                    if ack_dict[pkt[IP].dst] == pkt[IP].src:
                        # Checks if the value of the key(ip.dst) equals to the IP source address
                        # If this IP address(ip.dst) isn't suspicious so it Continues to next iteration,& does nothing.
                        continue
                else:
                    # This ip.dst is SUSPICIOUS
                    suspicious_ip_addresses_no_ack_list.append(pkt[IP].dst)

    # Condition checking- fast syn's
    for pkt in pcapFile:
        if TCP in pkt:
            if pkt[TCP].flags == SYN:
                # Checks the packet's TCP flag type is  SYN
                if pkt[IP].src in suspicious_ip_addresses_fast_syn_list:
                    # If it is, Checks if ip.src is  in suspicious ip's list: suspicious_ip_addresses_fast_syn_list
                    # If so it continues to the next iteration, and does nothing.
                    continue
                else:
                    # If the ip.src isn't in the suspicious ip's list
                    if pkt[IP].src in syn_ip_time_packets_dict:
                        # If so it checks if ip.src in dict
                        # If it is - checks if delta time is big enough
                        # By subtracting the packet's time value with the time value of that same ip.src we found
                        # in the dict, that value is assigned to the  actual_delta variable
                        actual_delta = syn_ip_time_packets_dict[pkt[IP].src] - pkt.time
                        # Checks if the subtraction is negative - if so it multiplies the value by -1
                        # ('cause it's a time difference value)
                        if actual_delta < 0:
                            actual_delta = actual_delta * -1
                        if actual_delta < delta_time:
                            # Checks if the time difference we found is NOT big enough, meaning if it's lesser then
                            # delta_time variable value.
                            # If so that ip.src is a suspicious ip address
                            # and it's added to the suspicious list
                            suspicious_ip_addresses_fast_syn_list.append(pkt[IP].src)
                            # In addition that IP address is removed  from the dict
                            # Because we already know it's suspicious and there's no need to check again for it.
                            syn_ip_time_packets_dict.pop(pkt[IP].src)
                        else:
                            # If the time difference value is big enough  that ip.src isn't suspicious
                            # and it is being updated with the new pkt's time value in the dict
                            syn_ip_time_packets_dict[pkt[IP].src] = pkt.time
                    else:
                        # If the pkt isn;t suspicious and isn't in the dict
                        # The ip.src is being added to the dict with it's pkt's time value
                        syn_ip_time_packets_dict[pkt[IP].src] = pkt.time
    # Removing duplicates from list: suspicious_ip_addresses_fast_syn_list
    suspicious_ip_addresses_fast_syn_list = list(dict.fromkeys(suspicious_ip_addresses_fast_syn_list))
    print("The num of suspicious ip addresses & fast syn is: " + str(len(suspicious_ip_addresses_fast_syn_list)))
    # Removing duplicates from list: suspicious_ip_addresses_no_ack_list
    suspicious_ip_addresses_no_ack_list = list(dict.fromkeys(suspicious_ip_addresses_no_ack_list))
    print("The num of suspicious ip addresses & no ack is: " + str(len(suspicious_ip_addresses_no_ack_list)))
    # The general sus ip addresses are the 2 lists mentioned above combined.
    suspicious_ip_addresses_list = suspicious_ip_addresses_fast_syn_list + suspicious_ip_addresses_no_ack_list
    print("The general num of suspicious ip addresses is: " + str(len(suspicious_ip_addresses_list)))
    # Writing the suspicious IP's into the file:  attackersListFile
    attackersListFile.write("The suspicious IP address are: " + "\n")
    for item in suspicious_ip_addresses_list:
        attackersListFile.write(item + "\n")
    # Closing the file.
    attackersListFile.close()


if __name__ == '__main__':
    main()
