
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DateTimeField
import datetime

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
  def __str__(self):
      return self.first_name + " " + self.last_name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(null=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(null=True, max_length=20, blank=True)
    bio = models.CharField(null=True, max_length=100, blank=True)

    def completed_courses(self):
        return Subscription.objects.filter(student=self, completed=True)

    def get_subscriptions(self):
        return Subscription.objects.filter(student=self, flag=True)
    

    def get_pending_meetings(self):
        subs = self.get_subscriptions().values('progress')
        return Meeting.objects.filter(week__in=subs)

    def get_unlocked_weeks(self, subscription):
        upto = subscription.progress.week_no+1
        return Week.objects.filter(course=subscription.course, week_no__level__lt=upto)

    def get_locked_weeks(self, subscription):
        upto = subscription.progress.week_no
        return Week.objects.filter(course=subscription.course, week_no__level__gt=upto)

    def __str__(self):
        return self.user.__str__()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/')
    bio = models.CharField(null=True, max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    photo = models.FileField(null=True, blank=True)
    phone = models.CharField(null=True, max_length=20, blank=True)
    approved = models.BooleanField(default=False)

    @property
    def all_courses(self):
        return Course.objects.filter(uploaded_by=self)

    @property
    def all_weeks(self):
        return Week.objects.filter(course__in=self.all_courses)
    


    def __str__(self):
        return self.user.first_name + " " + self.user.last_name



class Categories(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0.0)
    approved = models.BooleanField(default=False)
    approval_message = models.CharField(max_length=200, null=True, blank=True)
    @property
    def subscriptions(self):
        return Subscription.objects.filter(course=self).count()
    def get_all_questions(self):
        return Question.objects.filter(course=self).order_by('difficulty',)
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

class Week(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week_no = models.IntegerField()
    title = models.CharField(max_length=100, default="title")
    description = models.TextField(max_length=1000, null=True, blank=True)
    instructions = models.TextField(max_length=1000, null=True, blank=True)
    final = models.BooleanField(default=False)
    @staticmethod
    def get_files(week_id):
        print(week_id)
        return Files.objects.filter(week__id=week_id).only("file")

    @property
    def Questions(self):
        return Question.objects.filter(course=self.course)
    def __str__(self):
        return self.course.name + " week " + str(self.week_no)

class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subscribed_on = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    flag = models.BooleanField(auto_created=True,default=True)
    quiz_approve = models.BooleanField(auto_created=False, default=False)
    progress = models.ForeignKey(Week, on_delete=models.CASCADE)
    quiz_marks = models.FloatField(default=0)
    week_begin = models.DateField(auto_now_add=True, null=True)
    complete_date = models.DateField(null=True)
    quiz_count = models.IntegerField(default=0)

    @property
    def total_weeks(self):
        return Week.objects.filter(course=self.course).count()
    
    def set_quiz_marks(self, marks, question_count):
        m = (self.quiz_marks*self.quiz_count+marks/question_count)/(self.quiz_count+1)
        return m


    @property
    def next_unit(self):
        try:
            return Week.objects.get(course=self.course,week_no=(self.progress.week_no+1))
        except:
            if self.progress.final:
                return self
            else:
                return self

    def week_duration(self):
        diff = datetime.date.today()-datetime.date(year=self.week_begin.year, month=self.week_begin.month, day=self.week_begin.day)
        return diff.days

    def __str__(self):
        return self.course.name + " by " + self.student.user.username






class Files(models.Model):
    file = models.FileField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, null=True)

    

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

    @property
    def right_answer(self):
        if self.answer==1:
            return self.option_one
        elif self.answer==2:
            return self.option_two
        if self.answer==3:
            return self.option_three
        if self.answer==4:
            return self.option_four

    def __str__(self):
        return self.question

class Meeting(models.Model):
    meeting_on = models.DateTimeField()
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    link = models.CharField(max_length=500, null=True)

class Message(models.Model):
    message = models.TextField(max_length=1000)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.message

    