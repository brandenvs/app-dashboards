from django.shortcuts import render
from django.contrib.auth.decorators import login_required

app_label = 'portal'

@login_required(login_url='users:login')
def index(request):
    return render(request, 'portal.html')

def create_app(request):
    return render(request, 'create_app.html')
