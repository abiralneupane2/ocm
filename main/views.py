from . import models, forms
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import Files, User

# Create your views here.
def index(request):
    context = {
        'students': models.Student.objects.all().count(),
        'courses': models.Course.objects.all().count(),
        'universities': models.University.objects.all().count()
    }
    return render(request, 'index.html', context)

def dashboard(request):
    print(request.user.user_type)
    if request.user.is_authenticated:
        if request.user.user_type==1:
            student=request.user.student
            
            context={
                        'subscriptions': request.user.student.get_subscriptions(),
                        'student': student, 
                    }
            if request.method == 'GET':
                if request.GET.get('edit'):
                    context={
                        'subscriptions': request.user.student.get_subscriptions(),
                        'student': request.user.student, 
                        'profile_edit_form': forms.ProfileEditForm(instance=request.user.student),
                        'user_edit_form': forms.UserEditForm(instance=request.user),
                    }
                return render(request, 'student/dashboard.html', context)
            elif request.method == 'POST':
                pf = forms.ProfileEditForm(request.POST, request.FILES, instance=request.user.student)
                uf = forms.UserEditForm(request.POST, instance=request.user)
                if pf.is_valid() and uf.is_valid():
                    uf.save()
                    pf.save()
                else:
                    print(pf.errors)
                    print(uf.errors)

                
                return render(request, 'student/dashboard.html', context)
        elif request.user.user_type==2:
            teacher=request.user.teacher
            context={
                        'courses': teacher.all_courses,
                        'teacher': teacher, 
                    }
            if request.method == 'GET':
                if request.GET.get('edit'):
                    context={
                        'courses': teacher.all_courses,
                        'teacher': teacher, 
                        'profile_edit_form': forms.TeacherProfileEditForm(instance=teacher),
                        'user_edit_form': forms.UserEditForm(instance=request.user),
                    }
                return render(request, 'teacher/dashboard.html', context)
            elif request.method == 'POST':
                pf = forms.ProfileEditForm(request.POST, request.FILES, instance=request.user.teacher)
                uf = forms.UserEditForm(request.POST, instance=request.user)
                if pf.is_valid() and uf.is_valid():
                    uf.save()
                    pf.save()

                else:
                    print(pf.errors)
                    print(uf.errors)
                return render(request, 'teacher/dashboard.html', context)


        
        
    else:
        return redirect(reverse('index'))


def browse(request):
    context = {
        'courses' : models.Course.objects.all(),
        
        'categories': models.Course.get_all_categories(),
        'universities': models.University.objects.all()
    }
    return render(request, 'browse.html', context)

def course(request, id):
    if request.method=='POST':
        student = models.Student.objects.get(user=request.user)
        id = request.POST.get('course_id')
        course = models.Course.objects.get(id=id)
        try:
            s = models.Subscription.objects.get(student=student, course=course)
            
            s.flag = not s.flag
            
            s.save()
            
        except:
            s = models.Subscription(student=student, course=course).save()
    context={
        'course' : models.Course.objects.get(id=id)
    }
    return render(request, 'course.html', context)

def userlogin(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'login.html', {'form': forms.LoginForm()})
    else:
        if request.method == 'POST':
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                username  = form.cleaned_data.get("username")
                password  = form.cleaned_data.get("password")
                print(username)
                print(password)
                user = User.objects.get(username=username, password=password)
                print(user)
                if user is not None:
                    
                    login(request, user)        
                    print('user found')
                    return redirect(reverse('index'))
                    
                else:
                    print('not found')
                    return render(request, 'login.html', {'errmsg': "user not found", "form": form})
            else:
                print(form.errors)
        return render(request,'login.html', {'form': forms.LoginForm()})

def university(request, name):
    return render(request, 'university.html', { 'university': models.University.objects.get(name=name)})

def study(request, id):
    

    s=models.Course.objects.get(id=id)
    context={
        'subject': s,
        'subscription': models.Subscription.objects.get(course=s, student=request.user.student),
        'weeks': models.Week.objects.filter(course=s),
        
    }
    
    return render(request, 'sssh.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class Comment(View):
    
    def post(self, request):
        cmnt = request.POST.get('comment')
        id = request.POST.get('course_id')
        from_person = request.user.student
        in_course = models.Course.objects.get(id=id)
        models.FAQ(comment=cmnt, from_person=from_person, in_course=in_course).save()
        return HttpResponse(200)

    
    def delete(self, request):	
        body_unicode = request.body.decode('utf-8')
        id = body_unicode.split('=')[1]
        models.FAQ.objects.get(id=id).delete()
        return HttpResponse(200)


def quiz(request, week_id):
    if request.method=='POST':
        print(request.POST)
        id = models.Week.objects.get(id=week_id).course.id
        return redirect(reverse('study',  kwargs={'id':id}))
    week = models.Week.objects.get(id=week_id)
    questions = week.Questions
    context={
        'week': week,
        'questions': questions
    }
    return render(request, 'quiz.html', context)

def register(request):
    if request.method=='POST':
        sf = forms.StudentRegistrationForm(request.POST, request.FILES)
        
        uf = forms.UserRegistrationForm(request.POST)
        if uf.is_valid() and sf.is_valid():
            u=uf.save(commit=False)
            
            
            s=sf.save(commit=False)
            u.user_type=1
            s.user=u
            u.save()
            s.save()
        else:
            print(sf.errors)
            print(uf.errors)
            return HttpResponse("<p>error with form submission</p>")
        login(request, u)
        return redirect(reverse('dashboard'))
    context={
        'uform': forms.UserRegistrationForm(),
        'sform': forms.StudentRegistrationForm(),
        'tform': forms.TeacherRegistrationForm(),
    }
    return render(request, 'student/register.html', context)

def teacher_register(request):
    errormsg=""
    if request.method=='POST':
        sf = forms.TeacherRegistrationForm(request.POST, request.FILES)
        
        uf = forms.UserRegistrationForm(request.POST)
        if uf.is_valid() and sf.is_valid():
            u=uf.save(commit=False)
            
            
            s=sf.save(commit=False)
            u.user_type=2
            s.user=u
            
            u.save()
            s.save()
            print("saved")
            print(s.user)
        else:
            print(sf.errors)
            print(uf.errors)
            return HttpResponse("<p>error with form submission</p>")
        login(request, u)
        return redirect(reverse('dashboard'))
    context={
        'uform': forms.UserRegistrationForm(),
        'tform': forms.TeacherRegistrationForm(),
    }
    return render(request, 'teacher/register.html', context)


def add_course(request):
    if request.method=='POST':
        cform = forms.AddCourseForm(request.POST)
        fform = forms.StudyMaterialForm(request.POST, request.FILES)
        wform = forms.AddWeekForm(request.POST)
        if cform.is_valid():
            temp=cform.save(commit=False)
            temp.uploaded_by=request.user.teacher
            temp.save()
        if fform.is_valid():
            temp=fform.save(commit=False)
            temp.save()
        if wform.is_valid():
            temp=wform.save(commit=False)
            temp.save()
    cform = forms.AddCourseForm()
    wform = forms.AddWeekForm()
    wform.fields['course'].queryset = request.user.teacher.all_courses
    fform = forms.StudyMaterialForm()
    fform.fields['course'].queryset = request.user.teacher.all_courses
    fform.fields['week'].queryset = request.user.teacher.all_weeks
    context = {
        'cform': cform,
        'wform': wform,
        'fform': fform,
    }
    return render(request, 'teacher/add_course.html', context)