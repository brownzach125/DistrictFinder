import csv
import geocoder
import os
import sys
import utils

from Email.Email import send_email, create_message
from Maps import PinExtractor
from SunlightCongress import SunlightCongress


sender_name = "Zach Brown"
sender_email = "brownzach125@gmail.com"
message_subject = "A very important message"

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


def send_emails(entries):
    possible_emails = []
    for entry in entries:
        if entry['Email Opt Out'] != "No":
            print "Some one doesn't want an email"
            continue

        first_name = entry['First Name']
        last_name = entry['Last Name']
        email = entry['Email']

        # TODO You should add logic here  to decide which template to use
        # You can pass any key into the create_message function, as long as that key
        # is an entry in the template.
        message = create_message(template_folder=os.path.join("Email", "templates", "generic.txt"),
                                 sender_email=sender_email,
                                 sender_name=sender_name,
                                 to_name=first_name + " " + last_name,
                                 to_email=email,
                                 subject=message_subject)

        possible_emails.append({
            'sender_email': sender_email,
            'email': email,
            'message': message
        })

    for email in possible_emails:
        print "This is an email that will be sent"
        print "----------------------------------"
        print email['message']

        # TODO I'm pretty lazy about this you might make it better
        value = ""
        while(value != "Y" and value != "N"):
            value = raw_input("Enter Y/N:")
        if value == "Y":
            send_email(sender_email, email, message)
            print "Email sent!"

        print "----------------------------------"
        print


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
    active_chapters = filter(lambda chapter: chapter['status'] == "Active" or chapter['status'] == "In Progress",
                             PM_Chapters)
    # adds lat, lng, state and district to each dictionary in entries
    for item in entries:
        item.update(from_address_to_district(item['Address']))

    # determines closest chapter to the address given in each entry, adds this to dict under key 'chapter
    for item in entries:
        distance = sys.maxint
        if item['district'] == "N/A" or item['state'] == "N/A":
            continue

        for chapter in active_chapters:
            distance_new = utils.earth_arc_distance(chapter['lat'], chapter['lng'], item['Latitude'], item["Longitude"])
            if distance_new < distance:
                distance = distance_new
                item['Chapter'] = chapter['name']

    send_emails(entries)
    # if chapter['status'] == 'Targeted':
    #     distance_new = ((chapter['lat'] - item['Latitude']) ** 2 + (['lng'] - item['Longitude']) ** 2) ** .5
    #     if distance_new < distance:
    #         distance = distance_new
    #         item['target chapter'] = chapter['name']




    # filename = "Processed.csv"
    # with open(filename, 'wb') as f:
    #     w = csv.DictWriter(f, fieldnames)
    #     w.writeheader()
    #     w.writerows(entries)

if __name__ == "__main__":
    main()
