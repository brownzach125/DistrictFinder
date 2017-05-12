import geocoder
from SunlightCongress import SunlightCongress
import pprint
import csv
import sys


def from_address_to_district(location):
    g = geocoder.google(location)
    coords = g.latlng
    return SunlightCongress.get_district(*coords)


# filename = sys.argv[1]
filename = "test.csv"
# print filename
entries = []

with open(filename, 'rU') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        entries.append(row)

districts = [from_address_to_district(x['Address']) for x in entries]

print [x['district'] for x in districts]

# with open(filename,'wb') as f:
#     w = csv.writer(f)
#     w.writerow(header_names)
#     w.writerow(sums_list)
