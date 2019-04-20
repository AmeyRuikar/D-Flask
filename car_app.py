"""
car data apis
"""
import logging.config
import logging
import yaml

from flask import Flask, abort, jsonify, request, Response

# init logger
with open('./config/config.yml', 'r') as config:
    configs = yaml.safe_load(config)

logging.config.dictConfig(configs)
logger = logging.getLogger(__name__)

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
        logger.error('Request does not have all the required fields')
        return abort(500, 'All fields not present(or extra fields present). Expected fields{0}' \
                                                                    .format(list(required_fields)))

    car_info['cars'][new_car_info['type']].append({new_car_info['name']: \
                                    {'make': new_car_info['make'], 'price': new_car_info['price']}})

    return jsonify({'message': 'successfully added to /info data'})

@app.route('/apiMetadata')
def get_api_description():
    """
    describes the apis
    """
    logger.info('API metadata')
    contents = open('./resources/api/metadata.yaml').read()
    return Response(contents, mimetype='text/plain')

if __name__ == '__main__':
    app.run()
