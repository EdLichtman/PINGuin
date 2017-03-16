import json
from flask import Response

class ApiResponse():

    def appendPings(self, ping):
        request = ping.request
        response = { 'request' : { 'url' : request.url
                                   , 'method' : request.method
                                   , 'headers' : dict(request.headers)
                                   , 'body' : request.body}
                    , 'status_code' : ping.status_code
                    , 'headers' : dict(ping.headers) }
        self.pings.append(response)

    def getJSON(self):
        resp = Response(response= json.dumps({ 'result' : self.pings}),
                        status=200,
                        mimetype="application/json")
        return resp

    pings = []



