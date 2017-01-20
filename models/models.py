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