from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .service_spt import sync_records
import time
from .models import StudentProgress
from django.contrib import messages


app_label = 'hyperion'

def get_service(request):
    sync_records()    
    return HttpResponseRedirect(reverse('standalone:progression_tracker'))


def index(request):
    return HttpResponseRedirect(reverse('standalone:progression_tracker'))


def add_port(request):
    if request.method == 'POST':
        StudentProgress.objects.create(
            portfolio_url=request.POST.get('link') # Load portfolio url
        ).save() # Create new record

    time.sleep(2)
    get_service(request)

    return HttpResponseRedirect(reverse('standalone:progression_tracker'))


def delete_port(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        
        StudentProgress.objects.filter(
            fullname=fullname
        ).delete()
        
        messages.success(request, f'Successfully deleted student: {fullname}')
        messages.error(request, f'Student "{fullname}" not found.')

    time.sleep(2)
    get_service(request)

    return HttpResponseRedirect(reverse('standalone:progression_tracker'))


# def delete_port(request):
#     if request.method == 'POST':
#         fullname = request.POST.get('fullname')
#         StudentProgress.objects.filter(fullname=fullname).delete()

#     time.sleep(2)
#     return HttpResponseRedirect(reverse('standalone:progression_tracker'))

