from django.db.models import fields
from main import forms
from django.contrib import admin
from django import forms
from . import models
from .models import Teacher
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
admin.site.register(models.University)

admin.site.register(models.Student)
admin.site.register(models.Subscription)
admin.site.register(models.Week)
admin.site.register(models.Files)
admin.site.register(models.FAQ)
admin.site.register(models.Question)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Categories)

class TeacherAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeacherAdminForm, self).__init__(*args, **kwargs)
        self.fields['cv'].disabled = True
        self.fields['bio'].disabled = True
        self.fields['address'].disabled = True
        self.fields['photo'].disabled = True
        self.fields['phone'].disabled = True
    class Meta:
        model = Teacher
        exclude = ['user',]
    field_order = ['cv', 'photo', 'bio', 'address', 'phone', 'approved',]

class CourseAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseAdminForm, self).__init__(*args, **kwargs)
        self.fields['name'].disabled = True
        self.fields['uploaded_by'].disabled = True
        self.fields['description'].disabled = True
        self.fields['category'].disabled = True
    class Meta:
        model = models.Course
        fields = '__all__'
class TeacherAdmin(admin.ModelAdmin):
    exclude=['user',]
    form=TeacherAdminForm

admin.site.register(Teacher, TeacherAdmin)

class CourseAdmin(admin.ModelAdmin):
    exclude=['user',]
    form=CourseAdminForm

admin.site.register(models.Course, CourseAdmin)