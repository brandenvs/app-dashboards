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

        print(current_domain)

        if current_domain == 'stadprin.com':
            return HttpResponseRedirect(reverse('stadprin:index'))

        elif current_domain == 'bcodelabs.com':        
            return HttpResponseRedirect(reverse('portal:index'))

        # Default response
        response = self.get_response(request)
        return response
