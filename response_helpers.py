def package_ping(request, my_api_response):
    if (hasattr(request,"status_code")):
        if (200 <= request.status_code < 300):
            my_api_response.append_successful_pings(package_ping_html(request, "successful"))
        if (300 <= request.status_code < 400):
            my_api_response.append_redirection_pings(package_ping_html(request, "redirection"))
        if (400 <= request.status_code < 500):
            my_api_response.append_client_error_pings(package_ping_html(request, "client-error"))
        if (500 <= request.status_code):
            my_api_response.append_server_error_pings(package_ping_html(request, "server-error"))
    else:
        my_api_response.append_invalid_pings(package_error_html(request))

def package_ping_html(request, status_type):
    innerHTML = '<div class="ping ' + status_type + '">'
    innerHTML += '<div class="ping-url ' + status_type + '">' + request.url + '</div>'
    innerHTML += '<div class="ping-method ' +  status_type + '">' + request.request.method + '</div>'
    innerHTML += '<div class="ping-status ' + status_type + '">' + str(request.status_code) + '</div>'
    innerHTML += '<div class="ping-header ' + status_type + '">' + ','.join(request.headers) + '</div>'
    innerHTML += '</div>'
    return innerHTML

def package_error_html(request):
    innerHTML = '<div class="ping invalid-url">'
    innerHTML += '<div class="ping-url invalid-url">' + request.url + '</div>'
    innerHTML += '<div class="ping-method invalid-url">' + request.method + '</div>'
    innerHTML += '<div class="ping-status invalid-url">' + 'Error trying to connect to URL' + '</div>'
    innerHTML += '<div class="ping-header invalid-url">' + ','.join(request.headers) + '</div>'
    innerHTML += '</div>'
    return innerHTML

class api_response():

    def append_invalid_pings(self, ping):
        self.invalid_pings += ping

    def append_successful_pings(self, ping):
        self.successful_pings += ping

    def append_redirection_pings(self, ping):
        self.redirection_pings += ping

    def append_client_error_pings(self, ping):
        self.client_error_pings += ping

    def append_server_error_pings(self, ping):
        self.client_error_pings += ping

    def get_innerHTML(self):
        return "".join(
            [
                self.head,
                '<body>',
                self.invalid_pings,
                self.successful_pings,
                self.redirection_pings,
                self.client_error_pings,
                self.server_error_pings,
                '</body>'
            ])

    invalid_pings = ""
    successful_pings = ""
    redirection_pings = ""
    client_error_pings = ""
    server_error_pings = ""
    head = '<head><link rel="stylesheet" type="text/css" href="/css/styles.css"></head>'