
# class XContentOptionsMiddleware:
    # def __init__(self, get_response):
        # self.get_response = get_response

    # def __call__(self, request):
        # response = self.get_response(request)
        # response['X-Content-Type-Options'] = 'nosniff'
        # print("X-Content-Type-Options header set:", response['X-Content-Type-Options'])
        # return response
        
# In your base/middleware.py
class RemoveServerHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Server'] = 'MyAwesomeApp'  # Set a generic value
        print("Server header modified:", response['Server'])
        return response
        
class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the response already has a CSP header set
        if "Content-Security-Policy" not in response:
            # If not, set the CSP header with explicit directives
            response["Content-Security-Policy"] = (
                "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; frame-ancestors 'self'; form-action 'self';"
            )

        return response