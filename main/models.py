

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

GRADES = [
    ('A', 'Best'),
    ('B', 'Good')
]
class User(AbstractUser):
  USER_TYPE_CHOICES = ( 
      (1, 'student'),
      (2, 'teacher'),
      (3, 'admin'),
  )

  user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(null=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(null=True, max_length=20, blank=True)
    bio = models.CharField(null=True, max_length=100, blank=True)

    def get_subscriptions(self):
        return Subscription.objects.filter(student=self)
    
    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/')
    bio = models.CharField(null=True, max_length=100, blank=True)
    approved = models.BooleanField(default=False)
    address = models.CharField(max_length=100, blank=True)
    photo = models.FileField(null=True)
    phone = models.CharField(null=True, max_length=20, blank=True)

    @property
    def all_courses(self):
        return Course.objects.filter(uploaded_by=self)


    def __str__(self):
        return self.user.username

class University(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=20)



class Course(models.Model):
    name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)
    approval_message = models.CharField(max_length=200, null=True)
    @property
    def subscriptions(self):
        return Subscription.objects.filter(course=self).count()

    @property
    def faq(self):
        comments = FAQ.objects.filter(in_course=self)
        return comments

    @property
    def total_comments(self):
        return FAQ.objects.filter(in_course=self).count()


    @staticmethod
    def get_all_categories():
        return Course.objects.values_list('category', flat=True).distinct()
    @staticmethod
    def get_courses_by_categories(category):
        return Course.objects.filter(category=category)
    # @staticmethod
    # def get_courses_by_university(university):
        
    #     return Course.objects.filter(affiliated_to=university)
    
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

    @property
    def Questions(self):
        return Question.objects.filter(course=self.course)
    def __str__(self):
        return self.course.name + " week " + str(self.week_no)

class Files(models.Model):
    file = models.FileField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week = models.OneToOneField(Week, on_delete=models.CASCADE, null=True)

class FAQ(models.Model):
    from_person = models.ForeignKey(Student, on_delete=models.CASCADE)
    in_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.comment



class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    difficulty = models.IntegerField(default=1)
    question = models.CharField(max_length=100)
    option_one = models.CharField(max_length=20)
    option_two = models.CharField(max_length=20)
    option_three = models.CharField(max_length=20)
    option_four = models.CharField(max_length=20)
    answer = models.IntegerField(default=1)

    def __str__(self):
        return self.question

