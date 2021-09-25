from django import forms
from django.forms import fields

from .models import Student, Teacher, Course, Week, Files
from .models import User
from main import models




class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Id'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user',]

class TeacherProfileEditForm(forms.ModelForm):
    class Meta:
        model=Teacher
        exclude = ['user', 'approved',]

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class StudentRegistrationForm(forms.ModelForm):
    photo = forms.FileField(required=False)
    class Meta:
        model = Student
        exclude = ['user','bio']

class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('username','email','password', 'first_name', 'last_name','email')

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class TeacherRegistrationForm(forms.ModelForm):
    photo = forms.FileField(required=False)
    class Meta:
        model = Teacher
        fields = ('cv','address','photo','phone')

class AddCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ['approved', 'uploaded_by',]

class AddWeekForm(forms.ModelForm):
    
    class Meta:
        model = Week
        fields = '__all__'

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = '__all__'

class CourseEditForm(forms.ModelForm):
     class Meta:
        model = Course
        exclude = ['approved', 'uploaded_by','approval_message',]

class WeekEditForm(forms.ModelForm):
    class Meta:
        model = Week
        exclude = ['course', ]

class ScheduleMeetingForm(forms.ModelForm):
    meeting_on = forms.DateTimeField(
    input_formats=['%d/%m/%Y %H:%M'],
    )
    class Meta:
        model = models.Meeting
        fields = ['week', 'meeting_on']
    
class AllowQuizForm(forms.ModelForm):
    class Meta:
        model = models.Subscription
        fields = ['quiz_approve',]

class QuizManageForm(forms.ModelForm):
    class Meta:
        model = models.Question
        exclude = ['course',]
    field_order = ['question', 'option_one', 'option_two', 'option_three', 'option_four','answer', 'difficulty']

