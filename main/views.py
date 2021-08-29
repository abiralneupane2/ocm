from main import models
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
def index(request):
    return render(request, 'index.html')

def profile(request):
    if request.user.is_authenticated:
        context={
            'subscriptions': request.user.student.get_subscriptions(),
            'student': request.user.student
        }
        
        return render(request, 'profile1.html', context)
    else:
        return redirect(reverse('index'))


def browse(request):
    context = {
        'courses' : models.Course.objects.all(),
        'form': forms.BrowseForm(),
        'categories': models.Course.get_all_categories(),
        'universities': models.University.objects.all()
    }
    return render(request, 'browse.html', context)

def course(request, code):
    if request.method=='POST':
        student = models.Student.objects.get(user=request.user)
        code = request.POST.get('course_code')
        course = models.Course.objects.get(code=code)
        try:
            s = models.Subscription.objects.get(student=student, course=course)
            
            s.flag = not s.flag
            
            s.save()
            
        except:
            s = models.Subscription(student=student, course=course).save()
    context={
        'course' : models.Course.objects.get(code=code)
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
                user = User.objects.get(username=username)
                if user is not None:
                    if user.check_password(password):
                        login(request, user)        
                        print('user found')
                        return redirect(reverse('index'))
                    return render(request, 'login.html', {'errmsg': "password incorrect", "form": form})
                else:
                    print('not found')
                    return render(request, 'login.html', {'errmsg': "user not found", "form": form})
            else:
                print(form.errors)
        return render(request,'login.html', {'form': forms.LoginForm()})

def university(request, name):
    return render(request, 'university.html', { 'university': models.University.objects.get(name=name)})

def study(request, code):
    

    s=models.Course.objects.get(code=code)
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
        code = request.POST.get('course_code')
        print(code)
        from_person = request.user.student
        in_course = models.Course.objects.get(code=code)
        models.FAQ(comment=cmnt, from_person=from_person, in_course=in_course).save()
        return HttpResponse(200)

    
    def delete(self, request):	
        body_unicode = request.body.decode('utf-8')
        id = body_unicode.split('=')[1]
        models.FAQ.objects.get(id=id).delete()
        return HttpResponse(200)
