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




class DomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the host and check if the user was already redirected
        current_domain = request.get_host()
        already_redirected = request.session.get('already_redirected', False)

        # Define target paths based on the domain
        if current_domain == 'stadprin.com' and not already_redirected:
            request.session['already_redirected'] = True
            return HttpResponseRedirect(request, 'partials/standalone_home.html')


        elif current_domain == 'spt.bcodelabs.com' and not already_redirected:
            request.session['already_redirected'] = True
            return redirect('/portal')

        # Clear the redirect flag for future requests
        if already_redirected:
            request.session['already_redirected'] = False

        # Default response
        response = self.get_response(request)
        return response
