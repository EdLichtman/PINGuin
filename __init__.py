from flask import Flask
import os, json, requests

app = Flask(__name__)

home_directory = os.path.dirname(os.path.realpath(__file__))
ping_file = "pings.json"

def find_targets_to_ping_from_file():
    url_targets = open("/".join([home_directory,  ping_file]), "r").readlines()
    return  json.loads("".join(url_targets))

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
        url = target_to_ping["url"]

        if ('body' in target_to_ping):
            body = json.loads(target_to_ping["body"])
        else: body = None

        if ('headers' in target_to_ping):
            headers = json.loads(target_to_ping["headers"])
        else: headers = None

        if(target_to_ping["method"] == "GET"):
            request = requests.get(url, headers = headers)

            package_ping(request, response_object)

        if(target_to_ping["method"] == "POST"):
            if ("body" in vars()):
                data = body
            else:
                data = None
            request = requests.post(url,data, headers = headers)

            package_ping(request, response_object)


    return response_object.get_innerHTML()

if __name__ == "__main__":
	app.run()