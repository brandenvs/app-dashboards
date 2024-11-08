from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from hyperion.models import StudentProgress


app_label = 'standalone'


def index(request):
    return render(request, 'partials/standalone_home.html')

def progression_tracker(request):
    if request.user.is_authenticated:
        db_students = StudentProgress.objects.all()
        view_dict = {}

        _records = {}
        for student in db_students:

            if student.level == 'Level 1':              
                progress_lvl1 = int(student.completed) / 30 * 100
                resubmission_lvl1 = int(student.resubmitted) / 30 * 100
                incomplete_lvl1 = int(student.incomplete) / 30 * 100
                below100_lvl1 = int(student.below_100) / 30 * 100

                _records['lvl1_progress'] = round(progress_lvl1, 2)
                _records['lvl1_resubmission'] = round(resubmission_lvl1, 2)
                _records['lvl1_incomplete'] = round(incomplete_lvl1, 2)
                _records['lvl1_below100'] = round(below100_lvl1, 2)

            elif student.level == 'Level 2':
                progress_lvl2 = int(student.completed) * 23 / 100
                resubmission_lvl2 = int(student.resubmitted) / 30 * 100
                incomplete_lvl2 = int(student.incomplete) / 30 * 100
                below100_lvl2 = int(student.below_100) / 30 * 100

                _records['lvl2_progress'] = round(progress_lvl2, 2)
                _records['lvl2_resubmission'] = round(resubmission_lvl2, 2)
                _records['lvl2_incomplete'] = round(incomplete_lvl2, 2)
                _records['lvl2_below100'] = round(below100_lvl2, 2)

            elif student.level == 'Level 3':
                progress_lvl3 = int(student.completed) * 13 / 100
                resubmission_lvl3 = int(student.resubmitted) / 30 * 100
                incomplete_lvl3 = int(student.incomplete) / 30 * 100
                below100_lvl3 = int(student.below_100) / 30 * 100

                _records['lvl3_progress'] = round(progress_lvl3, 2) 
                _records['lvl3_resubmission'] = round(resubmission_lvl3, 2) 
                _records['lvl3_incomplete'] = round(incomplete_lvl3, 2) 
                _records['lvl3_below100'] = round(below100_lvl3, 2) 
                
                

            view_dict[student.fullname] = _records

        print(view_dict)
        return render(request, 'partials/student_progression.html', {'view_dict': view_dict})

    else:
        return HttpResponseRedirect(reverse('users:login'))
