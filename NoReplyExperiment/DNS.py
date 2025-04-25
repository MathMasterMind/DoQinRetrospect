import argparse
from scapy.all import IP, UDP, DNS, DNSQR, send

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Send a DNS query to the specified target.")
parser.add_argument("target_ip", help="The IP address of the target DNS server (e.g., 8.8.8.8).")
args = parser.parse_args()

# Target DNS server
target_ip = args.target_ip
target_port = 53  # Standard DNS port

# DNS query parameters
domain_name = "example.com"

# Create IP/UDP/DNS packet
ip_layer = IP(dst=target_ip)
udp_layer = UDP(sport=12345, dport=target_port)
dns_layer = DNS(rd=1, qd=DNSQR(qname=domain_name))  # rd=1 sets the "Recursion Desired" flag

# Combine and send
packet = ip_layer / udp_layer / dns_layer
send(packet, verbose=1)
