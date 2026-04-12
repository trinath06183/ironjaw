import requests

q = """
[out:json][timeout:25];
(
  node["sport"="boxing"](around:15000,28.5706333,77.3272147);
  way["sport"="boxing"](around:15000,28.5706333,77.3272147);
  node["sport"="martial_arts"](around:15000,28.5706333,77.3272147);
  way["sport"="martial_arts"](around:15000,28.5706333,77.3272147);
);
out body;
>;
out skel qt;
"""

data = requests.post('http://overpass-api.de/api/interpreter', data={'data': q}).json()
print("Number of gyms found:", len(data.get('elements', [])))
