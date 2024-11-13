from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email_address = models.EmailField()
    cell_number = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name

    
