import requests

def build_request(ping_object):
    request_object = {}

    request_object["url"] = ping_object["url"]
    request_object["method"] = ping_object["method"]

    if ('body' in ping_object):
        request_object["body"] = ping_object["body"]
    else:
        request_object["body"] = None

    if ('headers' in ping_object):
        request_object["headers"] = ping_object["headers"]
    else:
        request_object["headers"] = None

    return request_object


def make_request(request_info):
    try:
        if (request_info["method"] == "GET"):
            request = requests.get(request_info["url"],
                                   headers=request_info["headers"])

            return request

        if (request_info["method"] == "POST"):
            request = requests.post(request_info["url"],
                                    request_info["body"],
                                    headers=request_info["headers"])

            return request

        if (request_info["method"] == "PUT"):
            request = requests.put(request_info["url"],
                                   request_info["body"],
                                   headers=request_info["headers"])

            return request

        if (request_info["method"] == "DELETE"):
            request = requests.delete(request_info["url"],
                                      headers=request_info["headers"])

            return request
    except requests.exceptions.ConnectionError as err:
        return err.request