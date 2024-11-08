# redirect_middleware.py
from django.shortcuts import redirect
from django.conf import settings

class DomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the host from the request
        current_domain = request.get_host()

        print(current_domain)

        if current_domain == 'stadprin.com':

            return redirect('/welcome')
        elif current_domain == 'bcodelabs.com':
        
            return redirect('/portal')

        # Default response
        response = self.get_response(request)
        return response
