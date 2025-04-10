from netfilterqueue import NetfilterQueue
from scapy.all import IP, UDP

packet_count = 0  # Global count

def packet_filter(pkt):
    global packet_count

    scapy_pkt = IP(pkt.get_payload())

    if scapy_pkt.haslayer(UDP) and scapy_pkt[UDP].dport == 853:
        packet_count += 1
        if packet_count == 1:
            print("✅ Allowing first QUIC packet")
            pkt.accept()
        else:
            print("⛔ Dropping packet", packet_count)
            pkt.drop()
    else:
        pkt.accept()  # Let all other packets through

nfqueue = NetfilterQueue()
nfqueue.bind(1, packet_filter)

try:
    print("🎯 Packet filter running (allow 1 UDP:853 packet)")
    nfqueue.run()
except KeyboardInterrupt:
    print("🛑 Exiting.")
    nfqueue.unbind()
