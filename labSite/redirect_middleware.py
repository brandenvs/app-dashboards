# redirect_middleware.py
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse


class DomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the host from the request
        current_domain = request.get_host()

        potential_paths = ['/fetch-theme/', '/portal/', '/old-auth/?next=/portal/', '/?next=/portal/', '/', '/progression-tracker/', '/home/', '/signup/']

        print(current_domain)
        current_path = str(request.path)
        print(current_path)

        if current_domain == 'stadprin.com':
            current_path = str(request.path)

            if current_path == '/':
                return HttpResponseRedirect(reverse('stadprin:temp'))

        elif current_domain == 'spt.bcodelabs.com':
            current_path = str(request.path)
            
            if current_path not in potential_paths:
                return HttpResponseRedirect(reverse('portal:index'))

        # Default response
        response = self.get_response(request)
        return response
