import requests
import pandas as pd
import re


# get lon and lat geo coordinates
def get_geo_coordinates(row):
    # get geo coordinates via google api
    resp = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + re.sub("\s","%20",row['postal_code']) + "&json=1")
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception
    else:
        geo_data = resp.json()
        for result in geo_data['results']:
            long = result['geometry']['location']['lng']
            lat = result['geometry']['location']['lat']
        return pd.Series({'long': long, 'lat': lat})

# read and explore locations.csv
locations = pd.read_csv("locations.csv")
print(locations)
print(locations.info())

# assuming that the data is clean and that there are only exactly days between date_first and date_last
locations['days'] = (locations['date_last'] - locations['date_first']) / (60 * 60 * 24)

print(locations)

print(locations['postal_code'])

locations[["long", "lat"]] = locations.apply(get_geo_coordinates, axis=1)

print(locations)
