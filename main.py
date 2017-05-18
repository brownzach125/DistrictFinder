import geocoder
from SunlightCongress import SunlightCongress
import pprint
import csv
import sys
from Chapter import Chapter

filename = "Petro_Metro_Chapters.csv"

PM_Chapters = []

with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        PM_Chapters.append(Chapter(*row))


# print PM_Chapters

def from_address_to_district(location):
    g = geocoder.google(location)
    coords = g.latlng
    dict1 = {'Latitude': coords[0], 'Longitude': coords[1]}
    dict2 = SunlightCongress.get_district(*coords)
    dict1.update(dict2)
    return dict1


# filename = sys.argv[1]
filename = "test.csv"

entries = []

with open(filename, 'rU') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        entries.append(row)


for item in entries:
    item.update(from_address_to_district(item['Address']))

closest_chapter = 'Blank'
for item in entries:
    distance = 2 ^ 5
    for chapter in PM_Chapters:
        if item['district'] == chapter.district:
            distance_new = ((chapter.lat - item['Latitude']) ** 2 + (chapter.lng - item['Longitude']) ** 2) ** .5
            if distance_new < distance:
                distance = distance_new
                item['chapter'] = chapter.name

print entries
# fieldnames = entries[0].keys()

# with open(filename, 'wb') as f:
#    w = csv.DictWriter(f)
#    w.writeheader()
#    w.writerows(entries)
