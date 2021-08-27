from main.views import course, university
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
CATEGORIES = [
    ('WD', 'Web Development'),
    ('CN', 'Comuter Networking')
]
GRADES = [
    ('A', 'Best'),
    ('B', 'Good')
]

class University(models.Model):
    name = models.CharField(max_length=100)

    @property
    def courses(self):
        return Course.objects.filter(affiliated_to=self)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    affiliated_to = models.ForeignKey(University, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    category = models.CharField(choices=CATEGORIES, max_length=2, default='CN')
    code = models.CharField(max_length=3, default='000')

    @staticmethod
    def get_all_categories():
        return Course.objects.values_list('category', flat=True).distinct()
    @staticmethod
    def get_courses_by_categories(category):
        return Course.objects.filter(category=category)
    @staticmethod
    def get_courses_by_university(university):
        
        return Course.objects.filter(affiliated_to=university)
    
    def check_subscription(self, user):
        
        student = Student.objects.get(user=user)
        try:
            s=Subscription.objects.get(student=student, course=self)
            if s.flag==True:
                return True
            else:
                return False
        except:
            return False

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(null=True)

    def get_subscriptions(self):
        return Subscription.objects.filter(student=self)

    def __str__(self):
        return self.user.username

class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    completion = models.IntegerField(default=0)
    subscribed_on = models.DateField(auto_now_add=True)
    flag = models.BooleanField(auto_created=True, default=True)
    progress = models.IntegerField(default=0)

    @property
    def total_weeks(self):
        return Week.objects.filter(course=self.course).count()
    
    @property
    def next_unit(self):
        return Week.objects.get(course=self.course,week_no=(self.progress+1)).title

    def __str__(self):
        return self.course.name + " by " + self.student.user.username



class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    grade = models.CharField(choices=GRADES, max_length=2)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    def __str__(self):
        return self.student.user.username

class CertificateCourse(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Week(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week_no = models.IntegerField()
    title = models.CharField(max_length=100, default="title")

    def __str__(self):
        return self.course.name + " week " + str(self.week_no)

class Video(models.Model):
    video = models.FileField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.SET_NULL, null=True)