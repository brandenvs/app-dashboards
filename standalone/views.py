from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from hyperion.models import StudentProgress


app_label = 'standalone'


def index(request):
    return render(request, 'partials/standalone_home.html')


def progression_tracker(request):
    db_students = StudentProgress.objects.all()
    view_dict = {}
    chart_data = {
        'students': [],
        'level1': [],
        'level2': [],
        'level3': []
    }

    for student in db_students:
        if student.fullname not in chart_data['students']:
            chart_data['students'].append(student.fullname)
            _records = {}

        if student.level == 'Level 1':              
            progress_lvl1 = int(student.completed)  
            resubmission_lvl1 = int(student.resubmitted)
            incomplete_lvl1 = int(student.incomplete)
            below100_lvl1 = int(student.below_100)

            _records['lvl1_progress'] = progress_lvl1
            _records['lvl1_resubmission'] = resubmission_lvl1
            _records['lvl1_incomplete'] = incomplete_lvl1
            _records['lvl1_below100'] = below100_lvl1
            chart_data['level1'].append(progress_lvl1)

        elif student.level == 'Level 2':
            progress_lvl2 = int(student.completed)  
            resubmission_lvl2 = int(student.resubmitted)
            incomplete_lvl2 = int(student.incomplete)
            below100_lvl2 = int(student.below_100)

            _records['lvl2_progress'] = progress_lvl2
            _records['lvl2_resubmission'] = resubmission_lvl2
            _records['lvl2_incomplete'] = incomplete_lvl2
            _records['lvl2_below100'] = below100_lvl2
            chart_data['level2'].append(progress_lvl2)

        elif student.level == 'Level 3':
            progress_lvl3 = int(student.completed)  
            resubmission_lvl3 = int(student.resubmitted)
            incomplete_lvl3 = int(student.incomplete)
            below100_lvl3 = int(student.below_100)

            _records['lvl3_progress'] = progress_lvl3
            _records['lvl3_resubmission'] = resubmission_lvl3
            _records['lvl3_incomplete'] = incomplete_lvl3
            _records['lvl3_below100'] = below100_lvl3
            chart_data['level3'].append(progress_lvl3)

        view_dict[student.fullname] = _records

    return render(request, 'partials/student_progression.html', {
        'chart_data': chart_data,
        'records': view_dict
    })
