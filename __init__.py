from flask import Flask, send_from_directory, request as flask_request, abort
from response_helpers import *
from request_helpers import *
from models import *
from io_helpers import *

app = Flask(__name__, static_url_path='/static')

def ping_all_target_urls(list_of_targets_to_ping):
    response_object = api_response()
    for target_to_ping in list_of_targets_to_ping["urls"]:
        request_info = build_request(target_to_ping)

        request = make_request(request_info)

        package_ping(request, response_object)
    return response_object.get_innerHTML()

@app.route("/")
def api_root():
    return read_local_file("README.md")

@app.route("/", methods = ["POST"])
def api_POST():
    if (not hasattr(flask_request, "json")):
        return "This Route Requires a JSON Body"

    try:
        list_of_targets_to_ping = flask_request.json
    except:
        return "Please check that you're sending a body encoded with application/json"

    if "saveas" in list_of_targets_to_ping:
        file_name = list_of_targets_to_ping.pop("saveas", None)
        if file_name is not None:
            if not find_local_route_json(file_name):
                write_local_route_json(list_of_targets_to_ping, file_name)
            else:
                abort(409)

    return ping_all_target_urls(list_of_targets_to_ping)

@app.route('/<path:route>', methods = ["GET"])
def api_GET_route(route):
    list_of_targets_to_ping = read_local_route_json(route)
    if list_of_targets_to_ping is None:
        abort(404)

    return ping_all_target_urls(list_of_targets_to_ping)

@app.route('/<path:route>', methods = ["PUT"])
def api_PUT_route(route):
    if (not hasattr(flask_request, "json")):
        return "This Route Requires a JSON Body"

    try:
        list_of_targets_to_ping = flask_request.json
    except:
        return "Please check that you're sending a body encoded with application/json"

    if not "saveas" in list_of_targets_to_ping:
        if find_local_route_json(route):
            write_local_route_json(list_of_targets_to_ping, route)
        else:
            abort(404)
    else:
        abort(400, "Please remove saveas from your message body")

    return ping_all_target_urls(list_of_targets_to_ping)

@app.route('/<path:route>', methods = ["DELETE"])
def api_DELETE_route(route):
    if find_local_route_json(route):
        delete_local_route_json(route)
    else:
        abort(404)

    return "Route Successfully removed!"


@app.route('/css/<path:path>')
def api_GET_css(path):
    return send_from_directory(app.static_folder + '/css', path)


if __name__ == "__main__":
	app.run()