"""
Script to check which cities have boxing/martial arts centers
available in OpenStreetMap via Overpass API.
"""
import requests
import time

CITIES = [
    # India
    {"name": "Mumbai",       "lat": 19.0760, "lon": 72.8777},
    {"name": "Delhi",        "lat": 28.6139, "lon": 77.2090},
    {"name": "Bangalore",    "lat": 12.9716, "lon": 77.5946},
    {"name": "Chennai",      "lat": 13.0827, "lon": 80.2707},
    {"name": "Hyderabad",    "lat": 17.3850, "lon": 78.4867},
    {"name": "Kolkata",      "lat": 22.5726, "lon": 88.3639},
    {"name": "Pune",         "lat": 18.5204, "lon": 73.8567},
    {"name": "Ahmedabad",    "lat": 23.0225, "lon": 72.5714},
    {"name": "Jaipur",       "lat": 26.9124, "lon": 75.7873},
    {"name": "Noida",        "lat": 28.5355, "lon": 77.3910},
    {"name": "Lucknow",      "lat": 26.8467, "lon": 80.9462},
    {"name": "Surat",        "lat": 21.1702, "lon": 72.8311},
    {"name": "Faridabad",    "lat": 28.5706, "lon": 77.3272},
    {"name": "Chandigarh",   "lat": 30.7333, "lon": 76.7794},
    {"name": "Indore",       "lat": 22.7196, "lon": 75.8577},
    {"name": "Bhopal",       "lat": 23.2599, "lon": 77.4126},
    {"name": "Patna",        "lat": 25.5941, "lon": 85.1376},
    {"name": "Kochi",        "lat": 9.9312,  "lon": 76.2673},
    # Global
    {"name": "London",       "lat": 51.5074, "lon": -0.1278},
    {"name": "New York",     "lat": 40.7128, "lon": -74.0060},
    {"name": "Los Angeles",  "lat": 34.0522, "lon": -118.2437},
    {"name": "Tokyo",        "lat": 35.6762, "lon": 139.6503},
    {"name": "Dubai",        "lat": 25.2048, "lon": 55.2708},
    {"name": "Singapore",    "lat": 1.3521,  "lon": 103.8198},
    {"name": "Bangkok",      "lat": 13.7563, "lon": 100.5018},
    {"name": "Sydney",       "lat": -33.8688,"lon": 151.2093},
    {"name": "Paris",        "lat": 48.8566, "lon": 2.3522},
]

OVERPASS_URL = "http://overpass-api.de/api/interpreter"
RADIUS = 15000  # 15 km radius


def check_city(city):
    q = f"""
[out:json][timeout:20];
(
  node["sport"="boxing"](around:{RADIUS},{city['lat']},{city['lon']});
  way["sport"="boxing"](around:{RADIUS},{city['lat']},{city['lon']});
  node["sport"="martial_arts"](around:{RADIUS},{city['lat']},{city['lon']});
  way["sport"="martial_arts"](around:{RADIUS},{city['lat']},{city['lon']});
);
out body;
>;
out skel qt;
"""
    try:
        resp = requests.post(OVERPASS_URL, data={"data": q}, timeout=25)
        resp.raise_for_status()
        elements = resp.json().get("elements", [])
        named = [e for e in elements if "tags" in e and "name" in e["tags"]]
        return len(named), named
    except Exception as ex:
        return -1, []


print(f"\n{'='*60}")
print(f"{'CITY':<18} {'CENTERS':>7}  NAMES")
print(f"{'='*60}")

results = []
for city in CITIES:
    count, gyms = check_city(city)
    names = [g["tags"]["name"] for g in gyms[:3]]
    status = f"{count:>7}" if count >= 0 else "  ERROR"
    preview = ", ".join(names) if names else "(none with names)"
    print(f"{city['name']:<18} {status}  {preview}")
    results.append({"city": city["name"], "count": count, "names": [g["tags"]["name"] for g in gyms]})
    time.sleep(1.2)  # be polite to Overpass API

print(f"\n{'='*60}")
print("SUMMARY — Cities WITH centers (count > 0):")
print(f"{'='*60}")
for r in sorted(results, key=lambda x: x["count"], reverse=True):
    if r["count"] > 0:
        print(f"  {r['city']:<18} → {r['count']} center(s): {', '.join(r['names'][:5])}")

print("\nDone.")
