import requests
import json
import math

def get_current_location():
    """Fetches approximate coordinates based on your public IP."""
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5)
        data = response.json()
        loc = data.get('loc', '0,0').split(',')
        return float(loc[0]), float(loc[1]), data.get('city', 'Unknown City')
    except Exception as e:
        print(f"Error fetching IP location: {e}")
        return None, None, None

def haversine(lat1, lon1, lat2, lon2):
    """Calculates distance in kilometers between two points on Earth."""
    R = 6371.0 # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def fetch_nearby_gyms(lat, lon, radius_meters=15000):
    """
    Fetches boxing and martial arts gyms using OpenStreetMap's Overpass API.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["sport"="boxing"](around:{radius_meters},{lat},{lon});
      way["sport"="boxing"](around:{radius_meters},{lat},{lon});
      node["sport"="martial_arts"](around:{radius_meters},{lat},{lon});
      way["sport"="martial_arts"](around:{radius_meters},{lat},{lon});
    );
    out body;
    >;
    out skel qt;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        gyms = []
        for element in data.get('elements', []):
            if 'tags' in element and 'name' in element['tags']:
                el_lat = element.get('lat') or element.get('center', {}).get('lat')
                el_lon = element.get('lon') or element.get('center', {}).get('lon')
                
                # Try to extract from first node in geometry if the element is a way without center
                if not el_lat and 'geometry' in element and len(element['geometry']) > 0:
                     el_lat = element['geometry'][0].get('lat')
                     el_lon = element['geometry'][0].get('lon')

                # Calculate distance if we retrieved coordinates successfully
                distance = 999.9
                if el_lat and el_lon:
                    distance = haversine(lat, lon, float(el_lat), float(el_lon))

                gym_info = {
                    'name': element['tags']['name'],
                    'sport': element['tags'].get('sport', 'boxing/martial arts'),
                    'city': element['tags'].get('addr:city', 'Nearby'),
                    'street': element['tags'].get('addr:street', ''),
                    'distance_km': distance
                }
                gyms.append(gym_info)
                
        return gyms
    except Exception as e:
        print(f"Error fetching data from Overpass API: {e}")
        return []

if __name__ == "__main__":
    print("Attempting to determine your location based on IP address...")
    lat, lon, city = get_current_location()
    
    if lat and lon:
        print(f"Found location: {city} ({lat}, {lon})")
        print(f"Scanning a 15km radius for the 5 nearest centers...\n")
        
        results = fetch_nearby_gyms(lat, lon, radius_meters=15000)
        
        if results:
            # Sort by distance
            results.sort(key=lambda x: x['distance_km'])
            
            # Show top 5
            top_5 = results[:5]
            
            print(f"Top 5 Nearest Training Centers to You:")
            print("-" * 50)
            for idx, gym in enumerate(top_5, 1):
                location = f"{gym['street']}, {gym['city']}".strip(', ')
                if location == "Nearby": location = "Address not specified, but nearby"
                
                # Format distance
                dist_str = f"{gym['distance_km']:.2f} km" if gym['distance_km'] < 900 else "Distance unknown"
                
                print(f"{idx}. {gym['name']}")
                print(f"   Style: {gym['sport'].replace('_', ' ').title()}")
                print(f"   Distance: {dist_str}")
                print(f"   Location: {location}\n")
        else:
            print("No centers found within a 15km radius.")
    else:
        print("Could not determine your location.")
