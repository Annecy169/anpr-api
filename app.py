import json
from urllib.parse import parse_qs
from threading import Thread
from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response
from scraper import *

def api_handler(request):
    print('Incoming request')
    thr = Thread(target=carDetailsANPR, args=[])
    thr.start()

    print(carDetails)
    try:
        requestQuery = str(request).split(' HTTP/1.1')[0].split('/?')[1]
        numberplate = requestQuery.split('=')

        return { 
            "Received": 200,
            "Description": "Number Plate Received",
            numberplate[0]: numberplate[1]
        }
    except:
        return { 
            "Error": 404,
            "Required Content Type": "application/json",
            "Description": "Please add the following parameters",
            "Params": [
                {
                    "reg": "numberplate"
                }
            ]
        }


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('anpr', '/')
        config.add_view(api_handler, route_name='anpr', request_method='GET', renderer='json')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=3005)