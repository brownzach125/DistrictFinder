from pykml import parser
from os import path
import urllib
from zipfile import ZipFile

# Notice that this is pulling down a file from the web each time it runs. You'll need to have webconnection,
# though we could always store the file each time and have a version of the function that works offline if needed
def get_chapter_info():
    url = "http://www.google.com/maps/d/u/0/kml?mid=1tI3hy2BmZ7LCtmiVegW-D5YozoE"

    file_path = path.join(".", "test.kmz")

    urllib.urlretrieve(url,  file_path)


    kmz = ZipFile(file_path, 'r')

    chapters = []
    with kmz.open('doc.kml') as file:
        root = parser.parse(file).getroot()

        colors = {}
        for style in root.Document.Style:
            id = style.attrib['id']
            png = style.IconStyle.Icon.href.text
            if png == 'http://www.gstatic.com/mapspro/images/stock/22-blue-dot.png':
                colors[id] = "Active"
            if png == 'http://www.gstatic.com/mapspro/images/stock/157-yellow-dot.png':
                colors[id] = "In Progress"



        for folder in root.Document.Folder:
            for pm in folder.Placemark:
                if pm.name != folder.name:
                    if hasattr(pm, 'Point'):
                        chapters.append( {
                            "name": pm.name.text[:-12],
                            "lat": pm.Point.coordinates.text,
                            # TODO FORMAT STRING COORDINATES INTO TWO NUMBERS
                            #"district": folder.name.text,
                            "status": colors[pm.styleUrl.text.replace("#", "") + "-normal"]
                        }
                        )
    return chapters
#fileobject = urllib2.urlopen(url)
#root = parser.parse(fileobject).getroot()
#for folder in root.Document.Folder:
#    for pm in folder.Placemark:
#        if pm.name != folder.name:
#           if hasattr(pm, 'Point'):
#               print pm.name + pm.Point.coordinates
