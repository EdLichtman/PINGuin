from flask import abort

from helpers.io_helpers import *
from helpers.routing_helpers import ping_all_target_urls


def api_routing_GET(route):
    list_of_targets_to_ping = read_local_route_json(route)
    if list_of_targets_to_ping is None:
        abort(404)
    return ping_all_target_urls(list_of_targets_to_ping)

def api_routing_PUT(route, list_of_targets_to_ping):
    if not "saveas" in list_of_targets_to_ping:
        if alter_local_route_json(list_of_targets_to_ping, route):
            return ping_all_target_urls(list_of_targets_to_ping)
        else:
            abort(404)
    else:
        abort(400, "Please remove saveas from your message body")

def api_routing_DELETE(route):
    if delete_local_route_json(route):
        return "Route Successfully removed!"
    else:
        abort(404)