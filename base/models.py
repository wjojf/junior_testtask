from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=150)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, verbose_name='Course Descrtiption')
    start_date = models.DateTimeField(verbose_name='Course starts')
    end_date = models.DateTimeField(verbose_name='Course ends')    

    def __str__(self):
        return f'#{self.id} - {self.title}'

    class Meta:
        ordering = ['-start_date', '-end_date']


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    contact_email = models.EmailField()

    def __str__(self):
        return f'{str(self.user)}'
    
    class Meta:
        unique_together = ['user', 'course']