import json
from urllib.parse import parse_qs
from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response
from scraper import *

#handleProcess()

def api_handler(request):
    print('Incoming request')

    print(request)
    
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