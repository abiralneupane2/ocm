from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    affiliated_to = models.ForeignKey(University, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    completion = models.IntegerField(default=0)
    subscribed_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.course.name + " by " + self.student.name

