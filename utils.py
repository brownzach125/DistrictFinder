from math import acos, cos, sin, radians, sqrt, atan2


# Give me the angles in degrees
def earth_arc_distance(lat1, lon1, lat2, lon2):
    # Gives answer back in generic unit 1
    # Multiply by your sphere radius
    lat1 = radians(lat1 + 360)
    lon1 = radians(lon1 + 360)
    lat2 = radians(lat2 + 360)
    lon2 = radians(lon2 + 360)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    R = 3959
    a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    #ance = acos(cos(lat1) * cos(lat2) + sin(lat1) * sin(lat2) * cos(lon1 - lon2))
    return distance