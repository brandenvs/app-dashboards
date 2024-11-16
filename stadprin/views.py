from django.shortcuts import render
from .models import Contact
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def career(request):
    return render(request, 'career.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email_address = request.POST.get('email_address')
        cell_number = request.POST.get('contact_number')
        message = request.POST.get('message')
        
        # Save data to the Contact model
        contact = Contact(
            name=name,
            email_address=email_address,
            cell_number=cell_number,
            message=message
        )
        contact.save()
        return render(request, 'contact.html',{'message': 'Message has been sent! Please wait while we redirect you...'})
        # return HttpResponseRedirect(reverse('app:contact'), {'message': 'Message has been sent!'})
    return render(request, 'contact.html')


def gantt_chart(request):
    return render(request, 'apd_gantt_chart.html')
