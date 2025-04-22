import asyncio
import ssl
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm.asyncio import tqdm
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import ProtocolNegotiated
from aioquic.asyncio.protocol import QuicConnectionProtocol

import asyncio
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import ProtocolNegotiated

class DNSClient(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handshake_complete = asyncio.Event()
        self.handshake_failed = False
        self._timeout_handle = None

        # Schedule timeout in 1 second
        loop = asyncio.get_event_loop()
        self._timeout_handle = loop.call_later(0.1, self._on_timeout)

    def quic_event_received(self, event):
        if isinstance(event, ProtocolNegotiated):
            if not self.handshake_complete.is_set():
                self.handshake_complete.set()
            if self._timeout_handle:
                self._timeout_handle.cancel()

    def _on_timeout(self):
        if not self.handshake_complete.is_set():
            self.handshake_failed = True
            self.handshake_complete.set()  # Unblocks waiters
            self._quic.close(error_code=0x0, reason_phrase="Handshake timeout")


BASE_URL = "https://public-dns.info/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_json_links(url):
    print(f"Scraping: {url}")
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = set()
    json_links = []

    for tag in soup.find_all("a", href=True):
        text = tag.get_text(strip=True).lower()
        href = tag['href']
        full_url = urljoin(url, href)

        if "json" in text and href.endswith(".json"):
            json_links.append(full_url)

        if full_url.startswith(BASE_URL) and full_url != url:
            links.add(full_url)

    return json_links, links

def extract_ip_host_pairs(json_urls):
    pairs = []
    for url in json_urls:
        print(f"Downloading JSON: {url}")
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            for item in data:
                ip = item.get("ip")
                name = item.get("name") or ""
                if "," in name:
                    name = ""
                if ip:
                    pairs.append((ip, name))
        except Exception as e:
            print(f"Error parsing {url}: {e}")
    return pairs

async def check_doq(ip, server_name):
    # remove period from server_name if it exists
    server_name = server_name.rstrip('.')
    #print(f"Checking DoQ support for {ip} ({server_name})...")
    config = QuicConfiguration(is_client=True, alpn_protocols=["doq"])
    config.verify_mode = ssl.CERT_REQUIRED
    config.server_name = server_name

    for port in [8853, 853, 443]:
        try:
            async with connect(ip, port, configuration=config, create_protocol=DNSClient, wait_connected=True) as client:
                await asyncio.wait_for(client.handshake_complete.wait(), timeout=1)
                print("true")
                return True
        except Exception:
            continue
    
    return False

async def main():
    visited = set()
    all_json_links = []

    # Get JSON links and recurse one level
    page_json_links, links = get_json_links(BASE_URL)
    all_json_links.extend(page_json_links)
    visited.add(BASE_URL)

    for link in links:
        if link not in visited:
            sub_json_links, _ = get_json_links(link)
            all_json_links.extend(sub_json_links)
            visited.add(link)

    ip_name_pairs = extract_ip_host_pairs(all_json_links)
    # save the pairs to a file for later use
    with open("ip_name_pairs.txt", "w") as f:
        for ip, name in ip_name_pairs:
            f.write(f"{ip},{name}\n")

    # load pairs from file if needed
    with open("ip_name_pairs.txt", "r") as f:
        ip_name_pairs = [line.strip().split(",") for line in f if line.strip()]

    print(f"\nChecking {len(ip_name_pairs)} servers for DoQ support...\n")

    results = []
    
    size = 100
    for i in range(len(ip_name_pairs) // size):
        print(f"Checking batch {i+1} of {len(ip_name_pairs) // size + 1}...")

        tasks = [check_doq(ip, name) for ip, name in ip_name_pairs[i*size:(i+1)*size]]
        results.append(await tqdm.gather(*tasks))

    tasks = [check_doq(ip, name) for ip, name in ip_name_pairs[(len(ip_name_pairs) // size) * size:]]
    results.append(await tqdm.gather(*tasks))

    # Flatten the results list
    results = [item for sublist in results for item in sublist]

    with open("doq_json_results.csv", "w") as f:
        f.write("IP,Name,DoQ\n")
        for (ip, name), is_doq in zip(ip_name_pairs, results):
            if is_doq:
                print(f"{ip:15} | {name:40} | DoQ: ✅")
                f.write(f"{ip},{name},{is_doq}\n")


if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.run(check_doq("94.140.15.15", "dns.adguard-dns.com"))
    #asyncio.run(check_doq("209.164.189.54", "209-164-189-54.biz.static.teleguam.net"))
