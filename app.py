from flask import Flask
import matplotlib.pyplot as plt
from flask import request
import os
import random
import json
import pickle

import places
import sampling

def bootstrap(n):
    restaurants = places_cli.get_a_goodly_amount()
    dist = { r.id: sampling.RestaurantDistribution(r) for r in restaurants[:n] }
    return dist

places_cli = places.PlacesClient(os.getenv('GOOGLE_PLACES_API_KEY'))
distributions = bootstrap(5)

app = Flask(__name__)
@app.route('/api/sample', methods=['GET'])
def sample():
    result = sampling.sample(list(distributions.values()))
    return json.dumps({
        'restaurant': result['restaurant'].__dict__,
        'probabilities': result['probabilities']
    })

@app.route('/api/restaurants', methods=['GET'])
def restaurants():
    return json.dumps({
        'distributions': list(map(
            lambda d: {
                'distribution': d.distribution,
                'restaurant': d.restaurant.__dict__
            }, distributions.values()
        ))
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    for d in distributions.values():
        d.distribution = sampling.triangle_distribution(d.restaurant.rating / 5.0)
    return '{ "status": "ok" }'

@app.route('/api/update', methods=['POST'])
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
