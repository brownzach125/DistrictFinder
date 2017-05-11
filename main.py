import geocoder
from SunlightCongress import SunlightCongress

g = geocoder.google('2303 Milam St. Houston, Tx')

district = SunlightCongress.get_district(*g.latlng)
print district['state']
print district['district']
