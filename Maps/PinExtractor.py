from pykml import parser
from os import path
import urllib
from zipfile import ZipFile

# Notice that this is pulling down a file from the web each time it runs. You'll need to have webconnection,
# though we could always store the file each time and have a version of the function that works offline if needed
def get_chapter_info():
    url = "http://www.google.com/maps/d/u/0/kml?mid=1ALOQiOEpuJNHnU6vkeExBzjKFT8"

    file_path = path.join(".", "test.kmz")

    urllib.urlretrieve(url,  file_path)


    kmz = ZipFile(file_path, 'r')

    chapters = []
    with kmz.open('doc.kml') as file:
        root = parser.parse(file).getroot()

        for folder in root.Document.Folder:
            for pm in folder.Placemark:
                if pm.name != folder.name:
                    if hasattr(pm, 'Point'):
                        chapters.append( {
                            "name": pm.name.text,
                            "point": pm.Point.coordinates.text,
                            "district": folder.name.text
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