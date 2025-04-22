from scapy.all import *
import random

# Target DoT server
# target_ip = "94.140.14.14"
target_ip = "8.8.8.8"
target_port = 853
source_port = random.randint(1024, 65535)

# IP & initial SYN
ip = IP(dst=target_ip)
syn = TCP(sport=source_port, dport=target_port, flags="S", seq=1000)
synack = sr1(ip/syn, timeout=1)

if synack and synack.haslayer(TCP) and synack[TCP].flags == "SA":
    ack = TCP(
        sport=source_port,
        dport=target_port,
        flags="A",
        seq=synack.ack,
        ack=synack.seq + 1
    )
    send(ip/ack)

    # Craft a raw TLS ClientHello (minimal, no SNI)
    # adguard client hello
    # client_hello = bytes.fromhex(
    # "16030100ee010000ea0303cafdf38a72a68488bcd60e7152bfe76197adac2353f29551645ee08faae43926205f5eca23cc04ccd3dd07742318fb835baa9f69f48c82024a2c0df3f523149d48001cc02bc02fc02cc030cca9cca8c009c013c00ac014c01213011302130301000085000500050100000000000a000a0008001d001700180019000b0002010000230000000d001a0018080404030807080508060401050106010503060302010203ff010001000017000000120000002b00050403040303003300260024001d00200987c87ba8c538c7471f876affacdd2bb276a5ea6f3c7fe6f18a62715a62127e002d00020101"
    # )
    # google client hello
    client_hello = bytes.fromhex(
    "16030100ee010000ea030376f488d50dd6d70800915ea200f8ab310c9c24b5688505f91e04fa69bd63846f20a2d9eb554a8b546c46b0eb46492155e357a966170fbcc0f965066c12d2494f55001cc02bc02fc02cc030cca9cca8c009c013c00ac014c01213011302130301000085000500050100000000000a000a0008001d001700180019000b0002010000230000000d001a0018080404030807080508060401050106010503060302010203ff010001000017000000120000002b00050403040303003300260024001d00207c0a213ee69d39957fea4d5abaaba84b6561b7763b77854461e2ca9ae7456130002d00020101"
    )



    psh = TCP(
        sport=source_port,
        dport=target_port,
        flags="PA",
        seq=ack.seq,
        ack=ack.ack
    )
    send(ip/psh/client_hello)

    print("✅ SYN + ClientHello sent. No further replies will be ACKed.")
else:
    print("❌ No SYN-ACK received. Server might be unreachable.")
