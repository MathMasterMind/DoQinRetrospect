import argparse
from scapy.all import IP, TCP, send, RandShort

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Send a DNS over TLS packet to the specified target.")
parser.add_argument("target_ip", help="The IP address of the target (e.g., AdGuard, Cloudflare).")
args = parser.parse_args()

# Target DNS-over-TLS server
target_ip = args.target_ip
target_port = 853

# Create IP and TCP (SYN) packet
ip_layer = IP(dst=target_ip)
tcp_syn = TCP(
    sport=RandShort(),    # Random high source port
    dport=target_port,    # Destination port for DoT
    flags="S",            # SYN flag
    seq=1000              # Arbitrary sequence number
)

# Combine and send
packet = ip_layer / tcp_syn
send(packet, verbose=1)
