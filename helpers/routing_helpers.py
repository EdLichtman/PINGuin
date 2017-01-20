from helpers.response_helpers import package_ping
from helpers.request_helpers import make_request, build_request
from models.models import api_response


def ping_all_target_urls(list_of_targets_to_ping):
    response_object = api_response()
    for target_to_ping in list_of_targets_to_ping["urls"]:
        request_info = build_request(target_to_ping)

        request = make_request(request_info)

        package_ping(request, response_object)
    return response_object.get_innerHTML()