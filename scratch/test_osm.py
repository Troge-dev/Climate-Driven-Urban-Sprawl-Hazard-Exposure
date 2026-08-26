import urllib.request
import json
import os

query = """
[out:json][timeout:25];
(
  node["place"~"suburb|village|hamlet|neighbourhood|isolated_dwelling"](8.15,124.45,8.55,124.82);
);
out body;
"""
url = "https://overpass-api.de/api/interpreter"
req = urllib.request.Request(url, data=query.encode('utf-8'), headers={'User-Agent': 'DMA-UrbanSprawl-Research/1.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read().decode())
        elements = data.get("elements", [])
        print(f"Fetched {len(elements)} settlement points in CDO")
        for el in elements[:10]:
            print(el.get("tags", {}).get("name"), el.get("lat"), el.get("lon"), el.get("tags", {}).get("place"))
except Exception as e:
    print("Error:", e)
