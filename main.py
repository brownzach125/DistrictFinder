import geocoder
from SunlightCongress import SunlightCongress
import pprint
import csv
import sys
from Maps import PinExtractor
from Chapter import Chapter

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
filename = "New Members - TX Houston-West.csv"

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
    distance = 2 ^ 5
    if item['district'] == "N/A" or item['state'] == "N/A":
        continue
    for chapter in PM_Chapters:
        if (chapter['status'] == 'Active' or chapter['status'] == 'In Progress'):
            distance_new = ((chapter.lat - item['Latitude']) ** 2 + (chapter.lng - item['Longitude']) ** 2) ** .5
            if distance_new < distance:
                distance = distance_new
                item['Chapter'] = chapter.name
        if chapter.stat == 'Targeted':
            distance_new = ((chapter.lat - item['Latitude']) ** 2 + (chapter.lng - item['Longitude']) ** 2) ** .5
            if distance_new < distance:
                distance = distance_new
                item['target chapter'] = chapter.name
print entries


# fieldnames = ['First Name', 'Last Name', 'Email', 'Phone Number', 'Chapter', 'state', 'district', 'Address',
#               'target chapter', 'Longitude', 'Latitude', 'Emailed?', 'Called?']
#
# filename = "Processed.csv"
# with open(filename, 'wb') as f:
#     w = csv.DictWriter(f, fieldnames)
#     w.writeheader()
#     w.writerows(entries)
