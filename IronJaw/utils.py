import requests
import math
import time

# Use multiple Overpass mirrors for reliability
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]


def geocode_city(city_name):
    """Fetches coordinates for a given city name using Nominatim."""
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
    headers = {'User-Agent': 'IronJaw_App/1.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None


def haversine(lat1, lon1, lat2, lon2):
    """Calculates distance in kilometers between two points on Earth."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _post_overpass(query, timeout=25):
    """Try each Overpass mirror until one responds."""
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            resp = requests.post(
                endpoint,
                data={'data': query},
                timeout=timeout,
                headers={'User-Agent': 'IronJaw_App/1.0'}
            )
            if resp.status_code == 429:
                time.sleep(2)
                continue
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            print(f"Overpass endpoint {endpoint} failed: {e}")
            continue
    return None


def fetch_nearby_gyms(lat, lon, radius_meters=15000, ref_lat=None, ref_lon=None):
    """
    Fetches boxing/martial arts training centers via OpenStreetMap Overpass API.
    Runs two focused queries:
      1. sport-tagged nodes (boxing, martial_arts, karate, taekwondo, judo, kickboxing, mma)
      2. fitness/gym venues whose name contains combat-sport keywords
    Falls back to Overpass mirror servers if the primary is rate-limited.
    """
    # ── Query 1: venues explicitly tagged with a combat sport ──────────────
    q1 = f"""
[out:json][timeout:20];
(
  node["sport"~"boxing|martial_arts|karate|taekwondo|judo|kickboxing|mma",i](around:{radius_meters},{lat},{lon});
  way["sport"~"boxing|martial_arts|karate|taekwondo|judo|kickboxing|mma",i](around:{radius_meters},{lat},{lon});
);
out center body;
>;
out skel qt;
"""

    # ── Query 2: gyms/fitness centres whose name suggests combat sports ────
    q2 = f"""
[out:json][timeout:20];
(
  node["amenity"="gym"]["name"~"boxing|martial|karate|taekwondo|judo|kickbox|fight|combat|mma|ring|dojo|arena|muay",i](around:{radius_meters},{lat},{lon});
  way["amenity"="gym"]["name"~"boxing|martial|karate|taekwondo|judo|kickbox|fight|combat|mma|ring|dojo|arena|muay",i](around:{radius_meters},{lat},{lon});
  node["leisure"="fitness_centre"]["name"~"boxing|martial|karate|taekwondo|judo|kickbox|fight|combat|mma|ring|dojo|arena|muay",i](around:{radius_meters},{lat},{lon});
  way["leisure"="fitness_centre"]["name"~"boxing|martial|karate|taekwondo|judo|kickbox|fight|combat|mma|ring|dojo|arena|muay",i](around:{radius_meters},{lat},{lon});
  node["leisure"="sports_centre"]["name"~"boxing|martial|karate|taekwondo|judo|kickbox|fight|combat|mma|ring|dojo|arena|muay",i](around:{radius_meters},{lat},{lon});
  way["leisure"="sports_centre"]["name"~"boxing|martial|karate|taekwondo|judo|kickbox|fight|combat|mma|ring|dojo|arena|muay",i](around:{radius_meters},{lat},{lon});
);
out center body;
>;
out skel qt;
"""

    KEYWORDS = {
        'boxing', 'martial', 'karate', 'taekwondo', 'judo', 'kickbox',
        'fight', 'combat', 'mma', 'ring', 'dojo', 'arena', 'muay', 'bjj',
        'kung fu', 'wrestling', 'gym'
    }

    def _is_relevant(tags):
        sport = tags.get('sport', '').lower()
        name  = tags.get('name', '').lower()
        return any(k in sport or k in name for k in KEYWORDS)

    def _extract_coords(el):
        elat = el.get('lat') or el.get('center', {}).get('lat')
        elon = el.get('lon') or el.get('center', {}).get('lon')
        if not elat and el.get('geometry'):
            elat = el['geometry'][0].get('lat')
            elon = el['geometry'][0].get('lon')
        return elat, elon

    def _parse_elements(data):
        results = []
        for el in data.get('elements', []):
            tags = el.get('tags', {})
            name = tags.get('name', '').strip()
            if not name or not _is_relevant(tags):
                continue
            elat, elon = _extract_coords(el)
            dist = 999.9
            if elat and elon:
                rlat = ref_lat if ref_lat else lat
                rlon = ref_lon if ref_lon else lon
                dist = haversine(rlat, rlon, float(elat), float(elon))

            sport_raw = tags.get('sport', '')
            if not sport_raw:
                nl = name.lower()
                if 'boxing' in nl:       sport_raw = 'boxing'
                elif 'karate' in nl:     sport_raw = 'karate'
                elif 'taekwondo' in nl:  sport_raw = 'taekwondo'
                elif 'judo' in nl:       sport_raw = 'judo'
                elif 'mma' in nl:        sport_raw = 'mma'
                elif 'muay' in nl:       sport_raw = 'muay thai'
                elif 'dojo' in nl:       sport_raw = 'martial arts'
                else:                    sport_raw = 'martial arts'

            city_tag   = tags.get('addr:city') or tags.get('addr:town') or tags.get('addr:suburb') or ''
            street_tag = tags.get('addr:street', '')

            results.append({
                'name':        name,
                'sport':       sport_raw,
                'city':        city_tag if city_tag else 'Nearby',
                'street':      street_tag,
                'distance_km': dist,
                'lat':         float(elat) if elat else None,
                'lon':         float(elon) if elon else None,
            })
        return results

    all_gyms = []
    seen_names = set()

    for query in [q1, q2]:
        data = _post_overpass(query)
        if data:
            for g in _parse_elements(data):
                if g['name'] not in seen_names:
                    seen_names.add(g['name'])
                    all_gyms.append(g)

    all_gyms.sort(key=lambda x: x['distance_km'])
    return all_gyms[:20]
