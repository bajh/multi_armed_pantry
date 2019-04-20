import requests
from collections import namedtuple
import json
import sys

Result = namedtuple('Result', ['restaurants', 'pagetoken'])
Restaurant = namedtuple('Restaurant', ['id', 'name', 'vicinity', 'rating'])

class PlacesClient():

    def __init__(self, api_key):
        self.api_key = api_key
        self.default_location = '40.691340,-73.985163'
        self.default_radius = 1000

    def get(self, pagetoken=None, location=None, radius=None):
        base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        params = {
            'key': self.api_key,
            'location': location or self.default_location,
            'radius': radius or self.default_radius,
            'opennow': True,
            'type': 'restaurant',
            'pagetoken': pagetoken
        }

        r = requests.get(base_url, params=params)
        # TODO: handle this in some better way
        if r.status_code != 200:
            return None
        data = r.json()
        results = data.get('results', [])
        restaurants = list(map(lambda r: Restaurant(r['id'], r['name'], r['vicinity'], r['rating']), results))
        next_pagetoken = data.get('next_page_token', None)
        return Result(restaurants, next_pagetoken)

    def get_a_goodly_amount(self):
        restaurants = []
        pagetoken = None
        for _ in range(0, 5):
            result = self.get(pagetoken=pagetoken)
            pagetoken = result.pagetoken
            restaurants = restaurants + result.restaurants
            if pagetoken is None:
                return restaurants
        return restaurants