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
            current_path = str(request.path)

            if current_path != '/welcome/':
                return HttpResponseRedirect(reverse('stadprin:temp'))

        elif current_domain == 'spt.bcodelabs.com':
            current_path = str(request.path)
            
            if current_path != '/portal/':
                return HttpResponseRedirect(reverse('portal:index'))

        # Default response
        response = self.get_response(request)
        return response
