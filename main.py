import geocoder
from SunlightCongress import SunlightCongress
import pprint
import csv
import sys
from Maps import PinExtractor
from Chapter import Chapter
from math import acos, cos, sin, radians, sqrt, atan2


# Give me the angles in degrees
def earth_arc_distance(lat1, lon1, lat2, lon2):
    # Gives answer back in generic unit 1
    # Multiply by your sphere radius
    lat1 = radians(lat1 + 360)
    lon1 = radians(lon1 + 360)
    lat2 = radians(lat2 + 360)
    lon2 = radians(lon2 + 360)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    R = 3959
    a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    #ance = acos(cos(lat1) * cos(lat2) + sin(lat1) * sin(lat2) * cos(lon1 - lon2))
    return distance

# filename = "Petro_Metro_Chapters.csv"  # Local file on AS computer, not live
# cvs expected to have name, state, district, lat, lng, status of district in that order

#  Estalbish container for lists of chapters
# Current list is called PM for PetroMetro

PM_Chapters = []

# read chapter information from live CCL global map

PM_Chapters = PinExtractor.get_chapter_info()

# read chapter information from PetroMetro csv
# with open(filename, 'rU') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     for row in reader:
#         PM_Chapters.append(Chapter(*row))

# creates a new chapter object for each row in csv, stores in PM_Chapters



def from_address_to_district(location):
    """Takes a location (street address, zip code, city) and returns the latitude, longitude, and district as a dict"""
    g = geocoder.arcgis(location)
    coords = g.latlng
    dict1 = {'Latitude': g.lat, 'Longitude': g.lng}
    try:
        dict2 = SunlightCongress.get_district(*coords)
    except:
        dict2 = {u'state': u"N/A", u'district': u"N/A"}

    dict1.update(dict2)
    return dict1


# Filename of personnel data, expects more than one entry, should include headers
# filename = sys.argv[1]
filename = "Fake Member Data.csv"

entries = []  # holder for personnel dictionaries

# open personnel data csv, creates dictionary for each line
with open(filename, 'rU') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        entries.append(row)

# adds lat, lng, state and district to each dictionary in entries
for item in entries:
    item.update(from_address_to_district(item['Address']))

# determines closest chapter to the address given in each entry, adds this to dict under key 'chapter
closest_chapter = 'Blank'
for item in entries:
    distance = sys.maxint
    if item['district'] == "N/A" or item['state'] == "N/A":
        continue
    for chapter in PM_Chapters:
        if (chapter['status'] == "Active" or chapter['status'] == "In Progress"):
            distance_new = earth_arc_distance(chapter['lat'], chapter['lng'], item['Latitude'], item["Longitude"])
            if distance_new < distance:
                distance = distance_new
                item['Chapter'] = chapter['name']
        # if chapter['status'] == 'Targeted':
        #     distance_new = ((chapter['lat'] - item['Latitude']) ** 2 + (['lng'] - item['Longitude']) ** 2) ** .5
        #     if distance_new < distance:
        #         distance = distance_new
        #         item['target chapter'] = chapter['name']
print entries

#
# filename = "Processed.csv"
# with open(filename, 'wb') as f:
#     w = csv.DictWriter(f, fieldnames)
#     w.writeheader()
#     w.writerows(entries)
