from Maps import PinExtractor


class Chapter:
    def __init__(self, name, state, district, lat, lng, stat):
        self.name = name
        self.state = state
        self.district = int(district)
        self.lat = float(lat)
        self.lng = float(lng)
        self.stat = stat

    @classmethod
    def from_kml_data(cls, info):
        name = info["name"]
        state, district = tuple(info["district"].split('-'))
        lat, lng, _ = tuple(map(float,info["point"].strip().split(',')))
        stat = None
        # TODO I don't know what status is

        obj = cls(name, state, district, lat, lng, stat)
        return obj

    @staticmethod
    def load_chapters_from_map():
        return [ Chapter.from_kml_data(x) for x in PinExtractor.get_chapter_info()]

#chapters = Chapter.load_chapters_from_map()

