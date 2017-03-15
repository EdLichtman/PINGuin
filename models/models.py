import json, base64

class ApiResponse():

    def appendPings(self, ping):
        request = ping.request
        response = { "request" : { "url" : request.url
                                   , "method" : request.method
                                   , "headers" : dict(request.headers)
                                   , "body" : request.body}
                    , "status_code" : ping.status_code
                    , "headers" : dict(ping.headers)
                    , "content" : ping.text }
        self.pings.append(response)

    def getJSON(self):
        return json.dumps({ "result" : self.pings})

    pings = []



