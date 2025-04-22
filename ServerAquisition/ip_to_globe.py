import pandas as pd
import requests
import folium
from collections import defaultdict
import time
from tqdm import tqdm

# Load IPs
df = pd.read_csv("doq_json_results.csv")
ips = df["IP"].dropna().unique()

# Get IP geolocation
def get_ip_info(ip):
    try:
        resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "ip": ip,
                "country": data.get("country"),
                "org": data.get("org"),
                "loc": data.get("loc"),
            }
    except:
        return None

# Collect data
geo_data = []
for ip in tqdm(ips):
    info = get_ip_info(ip)
    if info and info["loc"]:
        geo_data.append(info)
    time.sleep(0.1)  # API-friendly pacing

# Group by location
location_map = defaultdict(list)
for entry in geo_data:
    location_map[entry["loc"]].append(entry)

# Build map
m = folium.Map(location=[20, 0], zoom_start=2)

for loc, servers in location_map.items():
    lat, lon = map(float, loc.split(","))
    count = len(servers)
    popup_text = f"{count} server(s)<br>"
    for s in servers:
        popup_text += f"{s['ip']} | {s.get('org', '')}<br>"

    folium.CircleMarker(
        location=(lat, lon),
        radius=5 + count * 0.3,  # scale circle size
        color="crimson",
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=300),
    ).add_to(m)

m.save("doq_server_clusters_map.html")
print("✅ Map saved to doq_server_clusters_map.html")
