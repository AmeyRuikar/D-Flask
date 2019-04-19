"""
car data apis
"""
import yaml
from flask import Flask, abort, jsonify, request

app = Flask(__name__)

# load intial set of data
car_info = yaml.safe_load(open('./resources/carInfo/staticInfo.yaml'))
required_fields = set(['type', 'name', 'make', 'price'])

@app.route('/')
def root_page():
    return '<h1>Get all the latest car information on \
                <a href="http://cardata/info">http://cardata/info</a> \
            <h1>'

@app.route('/info')
def get_car_info():
    """
    get data for cars based on types
    """
    # look for parameter
    if not request.args.get('type'):
        return jsonify(car_info)

    return jsonify(car_info.get('cars').get(request.args.get('type'), \
                                            {'message': 'Try some other type'}))

@app.route('/addInfo', methods=['POST'])
def add_car_info():
    """
    add for a new car
    """
    new_car_info = request.json

    if required_fields != set(new_car_info.keys()):
        return abort(500, 'All fields not present(or extra fields present). Expected fields{0}' \
                                                                    .format(list(required_fields)))

    car_info['cars'][new_car_info['type']].append({new_car_info['name']: \
                                    {'make': new_car_info['make'], 'price': new_car_info['price']}})

    return jsonify({'message': 'successfully added to /info data'})

if __name__ == '__main__':
    app.run()
