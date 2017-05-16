import geocoder
from SunlightCongress import SunlightCongress
import pprint
import csv
import sys
import Chapter


def from_address_to_district(location):
    g = geocoder.google(location)
    coords = g.latlng
    return SunlightCongress.get_district(*coords)


# filename = sys.argv[1]
filename = "test.csv"

entries = []

with open(filename, 'rU') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        entries.append(row)

for item in entries:
    item.update(from_address_to_district(item['Address']))

distance = 2 ^ 5
# for item in entries:
#   for chapter in PM_chapters:
#       if item['district']=chapter.district
#
#
fieldnames = entries[0].keys()

with open(filename, 'wb') as f:
    w = csv.DictWriter(f)
    w.writeheader()
    w.writerows(entries)
