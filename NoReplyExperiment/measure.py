from scapy.all import sniff, IP
from collections import defaultdict
import argparse
import csv

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Monitor network traffic to/from a specific IP address.")
parser.add_argument("target_ip", help="The target IP address to monitor.")
parser.add_argument("output_file", help="The CSV file to store results.")
args = parser.parse_args()

target_ip = args.target_ip
byte_counter = defaultdict(int)

# Initialize the CSV file and write headers if it doesn't exist
with open(args.output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Target IP', 'Sent (bytes)', 'Received (bytes)'])

def packet_callback(packet):
    if IP in packet:
        ip_layer = packet[IP]
        packet_len = len(packet)

        if ip_layer.src == target_ip:
            byte_counter["received"] += packet_len
        elif ip_layer.dst == target_ip:
            byte_counter["sent"] += packet_len

        # Write the current stats to CSV
        with open(args.output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([target_ip, byte_counter["sent"], byte_counter["received"]])

        print(f"Sent: {byte_counter['sent']} bytes, Received: {byte_counter['received']} bytes", end="\r")

print(f"Monitoring traffic to/from {target_ip}... Press Ctrl+C to stop.")
sniff(filter=f"ip host {target_ip}", prn=packet_callback, store=False)
