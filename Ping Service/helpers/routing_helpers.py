from helpers.request_helpers import make_request, build_request
from models.models import ApiResponse
from flask import abort



def ping_all_target_urls(list_of_targets_to_ping):
    response_object = ApiResponse()
    for target_to_ping in list_of_targets_to_ping["urls"]:
        request_info = build_request(target_to_ping)
        request = make_request(request_info)
        if (hasattr(request, "request")):
            response_object.appendPings(request)
        else:
            return abort(500, "Request was undeliverable")

    return response_object.getJSON()