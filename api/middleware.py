class RetalkHttpHeadersMiddleware(object):
    """ Add specific WWW-Authenticate header to 401 response
        (because some old android versions are awesome)
    """

    def process_response(self, request, response):
        if response.status_code == 401:
            response['WWW-Authenticate'] = 'Basic realm=""'
        return response
