import requests

sunlight_congress_domain = "https://congress.api.sunlightfoundation.com/legislators"


def get_district(latitude, longitude):
    payload = {
        "latitude": latitude,
        "longitude": longitude
    }

    request_str = sunlight_congress_domain + "/districts/locate"
    data = requests.get(request_str, params=payload).json()

    # TODO there is no error handling here :(
    return data['results'][0]


#get_district(29.748, -95.375)
