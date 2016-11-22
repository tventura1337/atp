import json

import bottle
from bottle import response
from main import airports_list, mdp
# app and routers

# the decorator
class EnableCors(object):

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            response.headers['Content-type'] = 'application/json'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = bottle.app()

@app.route('/airports/', methods=['GET'])
def get_all():
    return airports_list()

@app.route('/optimal/<source>/<destination>', method=['GET'])
def get_optimal(source, destination):
    return mdp(source, destination)

app.install(EnableCors())


    #return find("STL", "JFK")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, reloader=True, debug=True)
    