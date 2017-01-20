from flask import abort

from helpers.io_helpers import *
from helpers.routing_helpers import ping_all_target_urls


def api_root_GET(flask_request):
    return read_local_file("README.md")

def api_root_POST(list_of_targets_to_ping):

    if "saveas" in list_of_targets_to_ping:
        file_name = list_of_targets_to_ping.pop("saveas", None)
        if file_name is not None:
            if not write_local_route_json(list_of_targets_to_ping, file_name):
                abort(409)
    return ping_all_target_urls(list_of_targets_to_ping)
