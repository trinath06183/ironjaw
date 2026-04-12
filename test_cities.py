import sys
sys.path.insert(0, '.')
from IronJaw.utils import fetch_nearby_gyms, geocode_city

cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune']

for city in cities:
    lat, lon = geocode_city(city)
    if not lat:
        print(f"{city}: Could not geocode")
        continue
    gyms = fetch_nearby_gyms(lat, lon)
    print(f"\n{city} ({lat:.4f}, {lon:.4f}) -> {len(gyms)} centers:")
    for g in gyms:
        print(f"  - {g['name']} | {g['sport']} | {g['distance_km']:.1f}km")
