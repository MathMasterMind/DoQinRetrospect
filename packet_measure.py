from scapy.all import sniff, IP
from collections import defaultdict
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Monitor network traffic to/from a specific IP address.")
parser.add_argument("target_ip", help="The target IP address to monitor.")
args = parser.parse_args()

target_ip = args.target_ip
byte_counter = defaultdict(int)

def packet_callback(packet):
    if IP in packet:
        ip_layer = packet[IP]
        packet_len = len(packet)

        if ip_layer.src == target_ip:
            byte_counter["received"] += packet_len
        elif ip_layer.dst == target_ip:
            byte_counter["sent"] += packet_len

        print(f"Sent: {byte_counter['sent']} bytes, Received: {byte_counter['received']} bytes", end="\r")

print(f"Monitoring traffic to/from {target_ip}... Press Ctrl+C to stop.")
sniff(filter=f"ip host {target_ip}", prn=packet_callback, store=False)
