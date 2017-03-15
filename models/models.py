import json, flask

class ApiResponse():

    def appendPings(self, ping):
        response = { "status_code" : ping.status_code, "headers" : dict(ping.headers), "content" : ping.text}
        self.pings.append(response)

    def getJSON(self):
        return json.dumps(self.pings)

    pings = []



