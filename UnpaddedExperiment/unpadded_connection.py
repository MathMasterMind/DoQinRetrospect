import asyncio
import struct
from aioquic.asyncio.client import connect
from aioquic.quic.configuration import QuicConfiguration
from dnslib import DNSRecord
import ssl

DOQ_PORT = 853
QUERY_NAME = "google.com"

async def doq_query(resolver, name):
    # Prepare the DNS query
    dns_query = DNSRecord.question(QUERY_NAME).pack()
    query_payload = struct.pack("!H", len(dns_query)) + dns_query

    # QUIC client configuration
    config = QuicConfiguration(
        is_client=True, 
        alpn_protocols=["doq"], 
        verify_mode=ssl.CERT_REQUIRED, 
        server_name=name,
    )

    async with connect(resolver, DOQ_PORT, configuration=config) as protocol:
        # Create bidirectional stream
        stream_reader, stream_writer = await protocol.create_stream(is_unidirectional=False)

        # Send DNS query with 2-byte length prefix
        stream_writer.write(query_payload)
        await stream_writer.drain()
        stream_writer.write_eof()

        # Read the 2-byte length prefix
        length_bytes = await stream_reader.readexactly(2)
        response_len = struct.unpack("!H", length_bytes)[0]

        # Read the full DNS response
        response_data = await stream_reader.readexactly(response_len)

        # Parse and print DNS response
        response = DNSRecord.parse(response_data)
        #print("📥 DNS Response:")
        #print(response)
        print(f"Success: {resolver}")

# Get the resolver addresses from addresses.txt
with open("addresses.txt", "r") as f:
    for line in f:
        try:
            ip, hostname = [item.strip() for item in line.split(",")]
        except ValueError:
            print(f"⚠️ Skipping invalid line: {line}")

        try:
            asyncio.run(doq_query(ip, hostname))
        except Exception as e:
            print(f"Error querying {ip}")

