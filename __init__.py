from flask import Flask, send_from_directory
from response_helpers import *
from request_helpers import *
import os, json

app = Flask(__name__, static_url_path='/static')

home_directory = os.path.dirname(os.path.realpath(__file__))
ping_file = "pings.json"

def find_targets_to_ping_from_file():
    url_targets = open("/".join([home_directory,  ping_file]), "r").readlines()
    return  json.loads("".join(url_targets).replace("\n",""))

@app.route("/")
def api_root():
    response_object = api_response()
    list_of_targets_to_ping = find_targets_to_ping_from_file()
    
    for target_to_ping in list_of_targets_to_ping["urls"]:

        request_info = build_request(target_to_ping)

        request = make_request(request_info)

        package_ping(request, response_object)

    return response_object.get_innerHTML()


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(app.static_folder + '/css', path)


if __name__ == "__main__":
	app.run()