from scapy.all import IP, TCP, send, RandShort

# Target DNS-over-TLS server
target_ip = "94.140.14.14"
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
