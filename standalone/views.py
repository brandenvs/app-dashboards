from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from hyperion.models import dbStudent


app_label = 'standalone'


def index(request):
    return render(request, 'partials/standalone_home.html')

def progression_tracker(request):
    if request.user.is_authenticated:
        db_students = dbStudent.objects.all()

        return render(request, 'partials/student_progression.html', {'db_students': db_students})

    else:
        return HttpResponseRedirect(reverse('users:login'))
