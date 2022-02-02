"""
Author: Sharome Burton
Date: 02/01/2022
Course: CMPS4553 - Spatial Data Structures
P01
"""

import json
import random

def randColor():
  """
  Generates random hex color string
  """
  r = lambda: random.randint(0,255)
  return ('#%02X%02X%02X' % (r(),r(),r())).lower()

def makeGeoJson():
  geoJson = {
  "type": "FeatureCollection",
  "features": []
  }

  return geoJson

def makePoint(city):
  """
  Makes a .geojson point (dictionary) out of city data
  """
  feature = {
    "type": "Feature",
    "properties": {
      "marker-color":randColor(),
      "marker-symbol": ''
    },
    "geometry": {
      "type": "Point",
      "coordinates": [0,0]
    }
  }

  for key,val in city.items():
    if key == 'latitude':
      feature['geometry']['coordinates'][1] = val
    elif key == 'longitude':
      if val < -70.0 and val > -125.0:
        feature['geometry']['coordinates'][0] = val
      else:
        return None
    else:
      feature['properties'][key] = val

  return feature
  
def get_max_cities(states):
  """
  Gets dictionary of cities with max population
  """

  max_cities = {}

  for state in states:
    max_city_pop = 0
    max_city = "empty"
    for city in states[state]:
      if int(city["population"]) > max_city_pop:
        max_city_pop = int(city["population"])
        max_city = city
    max_cities.update({state:max_city})

  return max_cities

def makeCoord(coords):
  """
  Makes .geojson LineString (dictionary) from 
  list of tuples (lat, long, city) format
  """
  feature = {
    "type": "Feature",
    "properties": {
      "marker-color":randColor(),
      "marker-symbol": ''
    },
    "geometry": {
      "type": "LineString",
    "coordinates":[]
    }
  }

  for lat, long, city in coords:
      feature['geometry']['coordinates'].append([lat,long])
    
  return feature

# Change path as appropriate
with open("cities_latlon_w_pop.json") as f:
  data = json.load(f)

states = {}

for item in data:
  if not item["state"] in states:
    states[item["state"]] = []

  states[item["state"]].append(item)

# print(states)

# for state in states:
#   print(f"{state} = {len(states[state])}")

max_cities = get_max_cities(states)

# print(max_cities)
print(len(max_cities))    
# print(max_cities.keys())

cityInfo = []

for key, val in max_cities.items():
  # print(val)
  cityInfo.append(val)

# print(cityInfo)

points = [] # High pop cities
coords = [] # Coordinates of these cities

for city in cityInfo:
   points.append(makePoint(city))
   if city["longitude"] < -70.0 and city["longitude"] > -125.0:
    coords.append((city["longitude"], city["latitude"], city["city"]))

# print(coords)
coords.sort(reverse=True)
print(coords)

geoJsonCoords = makeCoord(coords)

# Prepare for new .geojson file
geoJson = makeGeoJson()

for point in points:
  if point != None:
    geoJson["features"].append(point)

geoJson["features"].append(geoJsonCoords)

# Write to new .geojson file
with open("new_geojson.geojson","w") as f:
  # json.update(points,f,indent=4)
  json.dump(geoJson,f,indent=4)


  
  