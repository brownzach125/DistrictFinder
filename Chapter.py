from Maps import PinExtractor


class Chapter:
    def __init__(self, name, state, district, lat, lng, stat):
        self.name = name
        self.state = state
        self.district = int(district)
        self.lat = float(lat)
        self.lng = float(lng)
        self.stat = stat

    # TODO  add population field that knows the number of people added by single execution of program

# @classmethod
#    def from_kml_data(cls, info):
#        name = info["name"]
#        # TODO need to find this using lat and long
#        state, district = None, None
#        #state, district = tuple(info["district"].split('-'))
#        lat, lng, _ = tuple(map(float,info["point"].strip().split(',')))
#        # TODO this is just the style png which contains the color
#        stat = info['status']

#        obj = cls(name, state, district, lat, lng, stat)
#        return obj

#    @staticmethod
#    def load_chapters_from_map():
#        return [ Chapter.from_kml_data(x) for x in PinExtractor.get_chapter_info()]

#chapters = Chapter.load_chapters_from_map()
