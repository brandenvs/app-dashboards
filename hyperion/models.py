from django.db import models


class StudentProgress(models.Model):
    student_name = models.CharField(max_length=100)
    bootcamp = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    completed = models.IntegerField(default=0)
    incomplete = models.IntegerField(default=0)
    resubmitted = models.IntegerField(default=0)
    below_100 = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student_name} - {self.bootcamp} - {self.level}"
