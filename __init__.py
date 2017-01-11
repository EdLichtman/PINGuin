from flask import Flask
import os, json, requests

app = Flask(__name__)

home_directory = os.path.dirname(os.path.realpath(__file__))
ping_file = "pings.json"

def find_targets_to_ping_from_file():
    url_targets = open("/".join([home_directory,  ping_file]), "r").readlines()
    return  json.loads("".join(url_targets))

def attr_is_none_type(request_object, attr):
    return ((attr in request_object and request_object[attr] is None)
            or attr not in request_object)

def build_request(ping_object):

    request_object = {}

    request_object["url"] = ping_object["url"]

    if ('body' in ping_object):
        request_object["body"] = json.loads(ping_object["body"])
    else:
        request_object["body"] = None

    if ('headers' in ping_object):
        headers = json.loads(ping_object["headers"])

        request_object["headers"] = headers
    else:
        request_object["headers"] = None

    if ('json_standard_headers' in ping_object):
        if (attr_is_none_type(request_object, 'headers')):
                request_object["headers"] = {}


        json_standard_headers = ping_object["json_standard_headers"]

        for header in json_standard_headers:
            request_object["headers"][header] = json_standard_headers[header]

    return request_object


def package_ping(request, my_api_response):
    if (request.status_code == 200):
        my_api_response.append_successful_pings(package_successful_ping(request))
    else:
        my_api_response.append_unsuccessful_pings(package_unsuccessful_ping(request))

def package_successful_ping(request):
    innerHTML = '<div class="pingUrl">' + request.url + '</div>'
    innerHTML += '<div class="ping-status">' + str(request.status_code) + '</div>'
    innerHTML += '<div class="ping-header">' + ','.join(request.headers) + '</div>'
    return innerHTML

def package_unsuccessful_ping(request):
    innerHTML = '<div class="pingUrl error">' + request.url + '</div>'
    innerHTML += '<div class="ping-status error">' + str(request.status_code) + '</div>'
    innerHTML += '<div class="ping-header error">' + ','.join(request.headers) + '</div>'
    return innerHTML

class api_response():

    def append_successful_pings(self, pings):
        self.successful_pings += pings

    def append_unsuccessful_pings(self, pings):
        self.unsuccessful_pings += pings

    def get_innerHTML(self):
        return "".join([self.unsuccessful_pings, self.successful_pings])

    successful_pings = ""
    unsuccessful_pings = ""

@app.route("/")
def api_root():
    response_object = api_response()
    list_of_targets_to_ping = find_targets_to_ping_from_file()
    for target_to_ping in list_of_targets_to_ping["urls"]:

        request_info = build_request(target_to_ping)

        if(target_to_ping["method"] == "GET"):
            request = requests.get(request_info["url"],
                                   headers = request_info["headers"])

            package_ping(request, response_object)

        if(target_to_ping["method"] == "POST"):
            request = requests.post(request_info["url"],
                                    request_info["body"],
                                    headers = request_info["headers"])

            package_ping(request, response_object)


    return response_object.get_innerHTML()

if __name__ == "__main__":
	app.run()