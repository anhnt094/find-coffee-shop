import json
import requests
import time
import yaml


def get_api_key():
    with open('/home/tuananh/my_api_key.yaml') as file:
        return yaml.load(file)['api_key']


def get_20_result(api_key,
                  keyword=None,
                  latitude=None,
                  longitude=None,
                  next_page_token=None,
                  return_type='json',
                  rankby='distance',
                  search_type='nearbysearch'):

    location = '{},{}'.format(latitude, longitude)
    if keyword and latitude and longitude:
        url = 'https://maps.googleapis.com/maps/api/place/{}/{}?location={}' \
              '&rankby={}&keyword={}&key={}'.format(search_type, return_type,
                                                    location, rankby, keyword,
                                                    api_key)
    else:
        url = 'https://maps.googleapis.com/maps/api/place/{}/{}'\
              '?&pagetoken={}&key={}'.format(search_type, return_type,
                                             next_page_token, api_key)

    resp = requests.get(url)

    return json.loads(resp.text)


def main():
    api_key = get_api_key()
    latitude = 10.779614
    longitude = 106.699256
    keyword = 'coffee'

    # while True:
    first_page = get_20_result(api_key, keyword, latitude, longitude)
    time.sleep(2)
    second_page = get_20_result(api_key,
                                next_page_token=first_page['next_page_token'])
    time.sleep(2)
    third_page = get_20_result(api_key,
                               next_page_token=second_page['next_page_token'])

    # Get 50 results
    results = first_page['results'] + second_page['results'] + \
        third_page['results'][:10]
    with open('/home/tuananh/hcm_coffee.json', 'wt') as file:
        json.dump(results, file, indent=4)


if __name__ == '__main__':
    main()
