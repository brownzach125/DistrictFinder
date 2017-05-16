class Chapter:
    def __init__(self, name, state, district, lat, lng, stat):
        self.name = name
        self.state = state
        self.district = district
        self.lat = lat
        self.lng = lng
        self.stat = stat


filename = "Petro_Metro_Chapters.csv"

PM_Chapters = []

# I want to be able to read a CSV....
# but instead of creating a new dict out of each row, create an instance of Chapter instead
