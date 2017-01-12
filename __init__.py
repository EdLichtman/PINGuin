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
        request_object["body"] = ping_object["body"]
    else:
        request_object["body"] = None

    if ('headers' in ping_object):
        request_object["headers"] = ping_object["headers"]
    else:
        request_object["headers"] = None

    return request_object


def package_ping(request, my_api_response):
    if (200 <= request.status_code < 300):
        my_api_response.append_successful_pings(package_ping_html(request, "successful"))
    if (300 <= request.status_code < 400):
        my_api_response.append_redirection_pings(package_ping_html(request, "redirection"))
    if (400 <= request.status_code < 500):
        my_api_response.append_client_error_pings(package_ping_html(request, "client-error"))
    if (500 <= request.status_code):
        my_api_response.append_server_error_pings(package_ping_html(request, "server-error"))

def package_ping_html(request, status_type):
    innerHTML = '<div class="ping-url ' + status_type + '">' + request.url + '</div>'
    innerHTML = '<div class="ping-method ' +  status_type + '">' + request.request.method + '</div>'
    innerHTML += '<div class="ping-status ' + status_type + '">' + str(request.status_code) + '</div>'
    innerHTML += '<div class="ping-header ' + status_type + '">' + ','.join(request.headers) + '</div>'
    return innerHTML

class api_response():
    def append_successful_pings(self, ping):
        self.successful_pings += ping

    def append_redirection_pings(self, ping):
        self.redirection_pings += ping

    def append_client_error_pings(self, ping):
        self.client_error_pings += ping

    def append_server_error_pings(self, ping):
        self.client_error_pings += ping

    def get_innerHTML(self):
        return "".join([self.successful_pings,
                        self.redirection_pings,
                        self.client_error_pings,
                        self.server_error_pings])

    successful_pings = ""
    redirection_pings = ""
    client_error_pings = ""
    server_error_pings = ""

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
                                    headers=request_info["headers"])

            package_ping(request, response_object)

        if(target_to_ping["method"] == "PUT"):
            request = requests.put(request_info["url"],
                                    request_info["body"],
                                    headers=request_info["headers"])

            package_ping(request, response_object)

        if(target_to_ping["method"] == "DELETE"):
            request = requests.delete(request_info["url"],
                                      headers=request_info["headers"])

            package_ping(request, response_object)

    return response_object.get_innerHTML()

if __name__ == "__main__":
	app.run()