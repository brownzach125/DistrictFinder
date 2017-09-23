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
    b = [7, 8, 9]
    a = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    daytime = list(itertools.product(a, b))
    for entry in entries:
        if entry['Email Opt Out'] != "No":
            print "Some one doesn't want an email"
            continue
        if entry['Contacted'] == "Yes":
            continue

        first_name = entry['First Name']
        last_name = entry['Last Name']
        email = entry['Email']
        GL_contact = entry['GL email']
        GL_name = entry['GL name']

        exactdaytime = daytime[count%12]

        count = count+1
        location = "Coco's at Gray and Baldwin in Midtown"

        if 'Chapter' not in entry:
                continue
        if entry['Assigned Chapter'] == "TX Katy-South":
            message = create_message(template_folder=os.path.join("Email", "templates", "questions_only.txt"),
                                     sender_email=sender_email,
                                     sender_name=sender_name,
                                     to_name=first_name + " " + last_name,
                                     to_email=email,
                                     subject=message_subject,
                                     salutation = first_name,
                                     GL_email = GL_contact,
                                     GL_name = GL_name)
        elif entry['Assigned Chapter'] in ["TX Houston-Montrose-Rice University", "TX Houston-Heights", "TX Houston-West University"]:
            message = create_message(template_folder=os.path.join("Email", "templates", "close_enough_for_coffee.txt"),
                                     sender_email=sender_email,
                                     sender_name=sender_name,
                                     to_name=first_name + " " + last_name,
                                     to_email=email,
                                     subject=message_subject,
                                     location=location,
                                     day=exactdaytime[0],
                                     time=exactdaytime[1],
                                     salutation = first_name,
                                     GL_email=GL_contact,
                                     GL_name=GL_name)
        else:
             message = create_message(template_folder=os.path.join("Email", "templates", "phone_call.txt"),
                                     sender_email=sender_email,
                                     sender_name=sender_name,
                                     to_name=first_name + " " + last_name,
                                     to_email=email,
                                     subject=message_subject,
                                     day=exactdaytime[0],
                                     time=exactdaytime[1],
                                     salutation = first_name,
                                     GL_email=GL_contact,
                                     GL_name=GL_name)

        possible_emails.append({
            'to_name': first_name,
            'email': email,
            'message': message,
            'chapter': entry['Chapter'],
            'GL_contact': GL_contact,
            'GL_name': GL_name
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
            send_email(sender_email, email['email'], email['GL_contact'], email['message'])
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
