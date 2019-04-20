from flask import Flask
from flask import request
import os
import random
import json

import places
import sampling

def bootstrap():
    restaurants = places_cli.get_a_goodly_amount()
    return { r.id: sampling.RestaurantDistribution(r) for r in restaurants }

places_cli = places.PlacesClient(os.getenv('GOOGLE_PLACES_API_KEY'))
distributions = bootstrap()

app = Flask(__name__)
@app.route('/sample', methods=['GET'])
def sample():
    restaurant = sampling.sample(list(distributions.values()))
    return json.dumps(restaurant)

@app.route('/update', methods=['POST'])
def update():
    val = request.args.get('val', '')
    restaurant_id = request.args.get('id', '')
    if val != '1' and val != '0':
        return '{ "status": "bad request" }', 400
    distribution = distributions.get(restaurant_id, None)
    if distribution is None:
        return '{ "status": "bad request" }', 400
    distribution.update(int(val))

    return '{ "status": "ok" }'

if __name__ == '__main__':
    app.run()
