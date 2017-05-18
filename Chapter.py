from Maps import PinExtractor


class Chapter:
    def __init__(self, name, state, district, lat, lng, stat):
        self.name = name
        self.state = state
        self.district = district
        self.lat = lat
        self.lng = lng
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

filename = "Petro_Metro_Chapters.csv"

PM_Chapters = []

# I want to be able to read a CSV....
# but instead of creating a new dict out of each row, create an instance of Chapter instead
