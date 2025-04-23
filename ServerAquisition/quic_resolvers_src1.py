import requests
import re
import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_quic_urls(html):
    # Regex to find quic://hostname[:port]/path
    return re.findall(r'quic://[a-zA-Z0-9\-._~%]+(?:\:\d+)?(?:/[^\s"<]*)?', html)

def resolve_hostnames(quic_urls):
    resolved = {}
    for url in quic_urls:
        try:
            # Parse out the hostname
            parsed = urlparse(url)
            hostname = parsed.hostname
            if hostname:
                #print(hostname)
                # Get all available IPs (IPv4 + IPv6)
                ip_list = []
                for info in socket.getaddrinfo(hostname, None):
                    ip = info[4][0]
                    if ip not in ip_list:
                        ip_list.append(ip)

                resolved[hostname] = ip_list
                for ip in ip_list:
                    print(f"{ip}, {hostname}")
            else:
                print(f"⚠️ Could not parse hostname from {url}")
        except Exception as e:
            print(f"⛔ Failed to resolve {url}: {e}")
    return resolved

def main():
    # Your target webpage
    target_url = "https://adguard-dns.io/kb/general/dns-providers/"  # 🔁 Replace with your real URL
    response = requests.get(target_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract raw HTML (some links might be embedded in JS or innerText)
    html = soup.prettify()
    
    # Step 1: Extract quic:// links
    quic_urls = extract_quic_urls(html)
    print(f"🔍 Found {len(quic_urls)} QUIC URLs")

    # Step 2: Remove duplicates by converting to a set
    quic_urls_unique = set(quic_urls)
    print(f"🔍 Found {len(quic_urls_unique)} unique QUIC URLs")

    # Step 3: Resolve them to IP addresses
    resolved = resolve_hostnames(quic_urls_unique)

    # Optional: Return or save
    return resolved

if __name__ == "__main__":
    main()
