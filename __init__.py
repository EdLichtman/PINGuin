from flask import Flask, send_from_directory, request as flask_request, abort
from response_helpers import *
from request_helpers import *
from models import *
from io_helpers import *

app = Flask(__name__, static_url_path='/static')



@app.route("/")
def api_root():
    response_object = api_response()
    return find_local_file("README.md")

@app.route("/", methods = ["POST"])
def api_post():
    if (not hasattr(flask_request, "json")):
        return "This Route Requires a JSON Body"

    try:
        list_of_targets_to_ping = flask_request.json
    except:
        return "Please check that you're sending a body encoded with application/json"

    if "saveas" in list_of_targets_to_ping:
        file_name = list_of_targets_to_ping.pop("saveas", None)
        if file_name is not None:
            write_input_to_file(list_of_targets_to_ping, file_name)

    response_object = api_response()

    for target_to_ping in list_of_targets_to_ping["urls"]:

        request_info = build_request(target_to_ping)

        request = make_request(request_info)

        package_ping(request, response_object)

    return response_object.get_innerHTML()

@app.route('/<path:route>')
def api_open_saved(route):
    response_object = api_response()
    try:
        list_of_targets_to_ping = find_local_json("/".join(["routes", route]))
    except:
        abort(404)

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