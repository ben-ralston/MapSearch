import csv

import requests
import json


api_key = "AIzaSyAqjEsJCbxsOlkz6Dj5XyMWETpu1Q_jh1c"


def getPLaceID(name, latitude, longitude, radius):
    request_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": name,
        "location": "{},{}".format(latitude, longitude),
        "radius": radius,
        "key": api_key,
    }

    response = requests.get(request_url, params=params)

    json_obj = response.json()
    if len(json_obj['results']) == 0:
        return 'None'

    first_result = json_obj['results'][0]

    if first_result['name'] == name:
        pass

    return first_result['place_id']

def main():
    # filename = input("Enter the name of a CSV file: ")
    filename = 'Junko Want to go.csv'

    with open(filename) as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)

        place_names = []
        for row in csv_reader:
            place_names.append(row[0])

    # print("\nYour Places:")
    # print(place_names[0:10])

    lat = "37.541290"
    lon = "-77.434769"
    radius = "75"

    names = [getPLaceID(name, lat, lon, radius) for name in place_names]
    print(names)



if __name__ == "__main__":
    main()

