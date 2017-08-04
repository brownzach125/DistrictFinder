import csv
import geocoder
import os
import sys
import utils

from Maps import PinExtractor
from SunlightCongress import SunlightCongress


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


def main():
    # Local file on AS computer, not live
    # csv expected to have name, state, district, lat, lng, status of district in that order
    if len(sys.argv) < 2:
        print "Input Data File Required"
        return -1

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print "{0} could not be opened".format(filename)
        return -1

    entries = []  # holder for personnel dictionaries

    # open personnel data csv, creates dictionary for each line
    with open(filename, 'rU') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            entries.append(row)

    #  Establish container for lists of chapters
    PM_Chapters = PinExtractor.get_chapter_info()

    # adds lat, lng, state and district to each dictionary in entries
    for item in entries:
        item.update(from_address_to_district(item['Address']))

    # determines closest chapter to the address given in each entry, adds this to dict under key 'chapter
    closest_chapter = 'Blank'

    active_chapters = filter(lambda chapter: chapter['status'] == "Active" or chapter['status'] == "In Progress",
                             PM_Chapters)
    for item in entries:
        distance = sys.maxint
        if item['district'] == "N/A" or item['state'] == "N/A":
            continue

        for chapter in active_chapters:
            distance_new = utils.earth_arc_distance(chapter['lat'], chapter['lng'], item['Latitude'], item["Longitude"])
            if distance_new < distance:
                distance = distance_new
                item['Chapter'] = chapter['name']

    # if chapter['status'] == 'Targeted':
    #     distance_new = ((chapter['lat'] - item['Latitude']) ** 2 + (['lng'] - item['Longitude']) ** 2) ** .5
    #     if distance_new < distance:
    #         distance = distance_new
    #         item['target chapter'] = chapter['name']
    print entries

    # filename = "Processed.csv"
    # with open(filename, 'wb') as f:
    #     w = csv.DictWriter(f, fieldnames)
    #     w.writeheader()
    #     w.writerows(entries)

if __name__ == "__main__":
    main()
