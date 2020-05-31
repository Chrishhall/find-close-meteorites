import math, requests

#This will calculate the distance between two points on the globe.
def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
      math.cos(lat1) * \
      math.cos(lat2) * \
      math.sin( (lon2 - lon1) / 2 ) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))

# This pulls the json file from NASA
meteor_resp = requests.get('https://data.nasa.gov/resource/gh4g-9sfh.json')


# meteor_resp.status_code # Validates the responce from the website "200" is good

# This translats the json information into a list of dictionaries
meteor_data = meteor_resp.json()

# Set my location tuple
my_loc = (39.079441,-104.872131)

for meteor in meteor_data:
    # Skips any meteor's with no location information
    if not ('reclat' in meteor and 'reclong' in meteor): continue
    # Calulates distancce from my location and adds to dictionary for each meteor
    meteor['distance']= calc_dist(float(meteor['reclat']),float(meteor['reclong']),my_loc[0],my_loc[1])

# Returns infinity if there is no distance value
def get_dist(meteor):
    return meteor.get('distance', 999999999) # The default value of math.inf did not work on my linux machine

# Shows how many entries are missing distance data
#len([m for m in meteor_data if 'distance' not in m ])

# Sort by distance and use above function to set anything without data to infinity
meteor_data.sort(key=get_dist)

# Show top ten closest meteor_resp
print(meteor_data[0:10])

# Showing just one value in the dictionary
#print(meteor_data[987])
