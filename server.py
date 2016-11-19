import json

from bottle import Bottle, HTTPError, request, template, route, static_file, view, redirect
from main import find
# app and routers
app = Bottle()

@app.route('/', method='GET')
def index():
    return find("STL", "JFK")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, reloader=True, debug=True)
    