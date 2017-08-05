import csv
import geocoder
import os
import sys
import utils
import itertools

from Email.Email import send_email, create_message
from Maps import PinExtractor
from SunlightCongress import SunlightCongress


sender_name = "Alex Summers"
sender_email = "3rdcoastccl@gmail.com"
message_subject = "Welcome to CCL!"

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
    count = 0
    b = [6, 7, 8]
    a = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    daytime = list(itertools.product(a, b))
    for entry in entries:
        if entry['Email Opt Out'] != "Yes":
            print "Some one doesn't want an email"
            continue

        first_name = entry['First Name']
        last_name = entry['Last Name']
        email = entry['Email']

        exactdaytime = daytime[count%12]

        count = count+1
        location = "Coco's at Gray and Baldwin in Midtown"

        invite1 = "speak with you, either on the phone or in person, to talk more about CCL and your interests." \
                  "Would you be available to talk over coffee or tea, at " + location + " on " + exactdaytime[1] + " at " + exactdaytime[2] +\
                  "? Please feel free to suggest a different location or time, " \
                  "I'm always interested in trying new local places and " \
                  "I'm happy to accommodate your schedule. Let me know what would be convenient for you."
        invite2 = "to speak with you to talk more about CCL and your interests. Would you be available to talk T Monday at 7? Please feel free to suggest a different time; I'm happy to accommodate your schedule."
        invite3 = "answer any questions you may have about CCL or our local activities."

        if entry['Chapter'] == "TX Katy-South":
            inviteme =invite3
        elif entry['Chapter'] == "TX Houston-Montrose-Rice University" or "TX Houston-Heights" or "TX Houston-West University":
            inviteme = invite1
        else:
            inviteme = invite2

        message = create_message(template_folder=os.path.join("Email", "templates", "generic.txt"),
                                 sender_email=sender_email,
                                 sender_name=sender_name,
                                 to_name=first_name + " " + last_name,
                                 to_email=email,
                                 subject=message_subject,
                                 invite=inviteme)

        possible_emails.append({
            'to_name': first_name, # TODO change to to_email
            'email': email,
            'message': message,
            'chapter': entry['Chapter']
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

if __name__ == "__main__":
    main()
