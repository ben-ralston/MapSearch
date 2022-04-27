import csv
import requests
import json

import pandas as pd


with open('key.txt') as file:
    api_key = file.read().strip()


def getPLaceID(name, latitude, longitude, radius):
    request_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = {
        'input': name,
        'inputtype': 'textquery',
        'fields': 'name,place_id,geometry/location',
        'locationbias': 'circle:{}@{},{}'.format(radius, latitude, longitude),
        'key': api_key,
    }

    response = requests.get(request_url, params=params)
    json_obj = response.json()

    if json_obj['status'] == 'ZERO_RESULTS':
        return False

    first_result = json_obj['candidates'][0]
    location = first_result['geometry']['location']

    place_dict = {
        'Name': first_result['name'],
        'Place ID': first_result['place_id'],
        'Latitude': float(location['lat']),
        'Longitude': float(location['lng']),
    }

    return place_dict


def createPlacesPickle():
    filename = 'Junko Want to go.csv'

    with open(filename) as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        place_names = [row[0] for row in csv_reader]

    places_df = pd.DataFrame(columns=['Name', 'Place ID', 'Latitude', 'Longitude'])

    lat = '37.541290'
    lon = '-77.434769'
    radius = '75'

    for name in place_names:
        place_dict = getPLaceID(name, lat, lon, radius)
        if not place_dict:
            continue

        places_df = places_df.append(place_dict, ignore_index=True)

    print(places_df)

    places_df.to_pickle('JunkosPlaces.pkl')


def searchPlaces(place_ids, search_params):
    request_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

    search_params['key'] = api_key

    response = requests.get(request_url, params=search_params)
    json_obj = response.json()

    next_page = json_obj['next_page_token']

    print('Results:', len(json_obj['results']))

    matching_results = []

    for result in json_obj['results']:
        if result['place_id'] in place_ids:
            matching_results.append({'name': result['name'],
                                     'rating': result['rating'],
                                     'number_of_reviews': result['user_ratings_total']
                                     })

    print(matching_results)

    # print(json_obj)


def main():
    places_df = pd.read_pickle('JunkosPlaces.pkl')
    place_ids = places_df['Place ID'].tolist()
    # print(place_ids)

    search = 'brewery'

    params = {
        'query': search,
        'location': '37.541290,-77.434769',
        'radius': '85000',
    }

    searchPlaces(place_ids, params)

    # createPlacesPickle()



if __name__ == '__main__':
    main()

