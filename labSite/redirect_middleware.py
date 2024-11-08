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
        # Define actions based on the domain
        if current_domain == 'stadprin.com':
            # Redirect to the appropriate view or URL for domain1
            return redirect('/welcome')  # Or serve a specific view
        elif current_domain == 'bcodelabs.com':
            # Redirect to the appropriate view or URL for domain2
            return redirect('/portal')  # Or serve a specific view

        # Default response
        response = self.get_response(request)
        return response
