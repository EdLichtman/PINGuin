from flask import Flask, request as flask_request
from helpers.io_helpers import create_routes_folder
from request_routes.routing_routes import api_root_GET, api_root_POST, api_routing_GET\
    , api_routing_PUT, api_routing_DELETE

import mysql.connector


app = Flask(__name__, static_url_path='/static')

@app.route("/", methods = ["GET","POST"])
def api_root():
    if flask_request.method == "GET":
        return api_root_GET(flask_request)
    if flask_request.method == "POST":
        if (not hasattr(flask_request, "json")):
            return "This Route Requires a JSON Body"
        try:
            list_of_targets_to_ping = flask_request.json
            if flask_request.json is None:
                abort(400, "Please check that you're sending a body encoded with application/json")
        except:
            abort(400, "Please check that you're sending a body encoded with application/json")
        return api_root_POST(list_of_targets_to_ping)

@app.route('/<path:route>', methods = ["GET", "PUT", "DELETE"])
def api_routing(route):
    if flask_request.method == "GET":
        return api_routing_GET(route)
    if flask_request.method == "PUT":
        if (not hasattr(flask_request, "json")):
            return "This Route Requires a JSON Body"
        try:
            list_of_targets_to_ping = flask_request.json
        except:
            return "Please check that you're sending a body encoded with application/json"
        return api_routing_PUT(route, list_of_targets_to_ping)
    if flask_request.method == "DELETE":
        return api_routing_DELETE(route)


if __name__ == "__main__":
  create_routes_folder()
  app.run()
