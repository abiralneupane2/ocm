from django.forms.formsets import formset_factory
from . import models, forms
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.forms.models import modelformset_factory
from .models import Files, Meeting, Student, Subscription, User
from main.forms import QuizManageForm
from main.utils import render_to_pdf
from django.template.loader import get_template
import datetime


# Create your views here.
def index(request):
    form = forms.IndexMessageForm()
    if request.method == 'POST':
        form = forms.IndexMessageForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'students': models.Student.objects.all().count(),
        'courses': models.Course.objects.all().count(),
        'teachers': models.Teacher.objects.all().count(),
        'form': form
    }
    return render(request, 'index.html', context)

def dashboard(request):
    print(request.user.user_type)
    if request.user.is_authenticated:
        if request.user.user_type==1:
            student=request.user.student
            
            context={
                        'subscriptions': request.user.student.get_subscriptions(),
                        'completed': models.Subscription.objects.filter(student=student, completed=True),
                        'student': student, 
                        'pending_meetings': student.get_pending_meetings(),
                    }
            if request.method == 'GET':
                if request.GET.get('edit'):
                    context={
                         
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
                        'meetings': models.Meeting.objects.filter(requested_by=request.user, completed=False),

                    }
            if request.method == 'GET':
                if request.GET.get('edit'):
                    context={
                         
                        'profile_edit_form': forms.TeacherProfileEditForm(instance=teacher),
                        'user_edit_form': forms.UserEditForm(instance=request.user),
                        
                    }
                elif request.GET.get('link'):
                    id=request.GET.get('meeting-id')
                    
                    mt = models.Meeting.objects.get(id=id)
                    link = request.GET.get('link')
                    mt.link=link
                    mt.save()
                
                elif request.GET.get('delete'):
                    id=request.GET.get('meeting-id')
                    mt = models.Meeting.objects.get(id=id).delete()
                
                elif request.GET.get('completed'):
                    id=request.GET.get('meeting-id')
                    mt = models.Meeting.objects.get(id=id)
                    mt.completed=True
                    mt.save()
                    
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
        'teachers': models.Teacher.objects.all()
    }
    return render(request, 'browse.html', context)

def course(request, id):
    course = models.Course.objects.get(id=id)
    if request.user.is_authenticated:
        if request.user.user_type==1:
            if request.method=='POST':
                student = models.Student.objects.get(user=request.user)
                
                try:
                    s = models.Subscription.objects.get(student=student, course=course)
                    
                    s.flag = not s.flag
                    
                    s.save()
                    
                except:
                    first_week = models.Week.objects.get(course=course,week_no=1)
                    s = models.Subscription(student=student, course=course, progress=first_week, flag=True).save()
            context={
                'course' : models.Course.objects.get(id=id)
            }
            return render(request, 'student/course.html', context)

        elif request.user.user_type==2:
            errmsg=" "
            if request.method=="POST":
                mtform = forms.ScheduleMeetingForm(request.POST)
                
                if mtform.is_valid():
                    f = mtform.save(commit=False)
                    f.requested_by=request.user
                    
                    f.save()
                else:

                    errmsg=mtform.errors
                    print(errmsg)

            mtform = forms.ScheduleMeetingForm()
            mtform.fields['week'].queryset = models.Week.objects.filter(course=course)
            context ={
                'course': course,
                'weeks': models.Week.objects.filter(course=course),
                'subscriptions': models.Subscription.objects.filter(course=course),
                'mtform': mtform,
                'errmsg': errmsg,
                
            }
            
            return render(request, 'teacher/course.html', context)
    else:
        context={
                'course' : course
            }
        return render(request, 'student/course.html', context)


def userlogin(request):
    errmsg = ""
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
                try:
                    user = User.objects.get(username=username, password=password)
                    login(request, user) 
                    return redirect(reverse('index'))
                except:
                    
                    return render(request, 'login.html', {'errmsg': "Username or password doesn't match", "form": form})

                
            else:
                print(form.errors)
                errmsg = form.errors
                render(request, 'login.html', {'errmsg': errmsg, "form": form})
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
    
    return render(request, 'student/sssh.html', context)


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

def start_lesson(request, week_id):
    week=models.Week.objects.get(id=week_id)
    c=week.course
    files=models.Files.objects.filter(week=week)
    s = models.Subscription.objects.get(student=request.user.student, course=c)
    context={
        'week': week,
        'files': files,
        'subscription': s,
    }
    return render(request, 'student/studying.html', context)

def edit_course(request, id):
    course = models.Course.objects.get(id=id)
    if request.method=="post":
        cf = forms.CourseEditForm(request.POST)
        weeks = models.Week.objects.filter(course=course)
        weekformsetfactory = modelformset_factory(models.Week, forms.WeekEditForm, extra=1)
        formset = weekformsetfactory(request.POST, queryset=weeks)
        if cf.is_valid():
            cf.save()
        formset.save()
        return redirect(reverse('course', kwargs={'id':id}))
    cf = forms.CourseEditForm(instance=course)
    weekformsetfactory = modelformset_factory(models.Week, forms.WeekEditForm, extra=1)
    weeks = models.Week.objects.filter(course=course)
    print(weeks)
    formset = weekformsetfactory(queryset=weeks)
    context={
        'course':course,
        'edit_course_form': cf,
        'edit_week_formset': formset,
    }
    return render(request, 'teacher/edit_course.html', context)

def quiz_approve(request, course_id, user_id):
    user=models.User.objects.get(id=user_id)
    s = models.Subscription.objects.get(course__id=course_id, student=user.student)
    print(s)
    if request.method=="GET":
        context = {
            'subscription': s,
            'form': forms.AllowQuizForm(instance=s)
        }
        
        return render(request, 'teacher/quiz_approve.html', context)

    if request.method=='POST':
        f = forms.AllowQuizForm(request.POST, instance=s)
        f.save()
        murl = reverse('course_details', kwargs={'id':course_id})
        return HttpResponse("Successfully updated. Go <a href="+murl+">back</a>")

def manage_quiz(request, course_id):
    errmsg = " "
    course = models.Course.objects.get(id=course_id)
    qf = modelformset_factory(models.Question, QuizManageForm, extra=1)
    if request.method=='POST':
        forms = qf(request.POST, queryset=course.get_all_questions())
        print(forms)
        if forms.is_valid():
            for f in forms.save(commit=False):
                f.course=course
                f.save()
        else:
            
            errmsg=forms.non_form_errors
        
    qs=course.get_all_questions()
    forms = qf(queryset=qs)
    context = {
        'forms': forms,
        'course': course,
        'errmsg': errmsg,
    }
    return render(request, 'teacher/manage_quiz.html', context)

def take_quiz(request, week_id):
    wk = models.Week.objects.get(id=week_id)
    q = models.Question.objects.filter(difficulty=wk.week_no)

    if request.method == 'POST':
        question_count = int(request.POST.get("question-count"))
        print(question_count)
        count=0
        for t in q:
            a=request.POST.get(str(t.id))
            if a==t.right_answer:
                count=count+1
        sub = models.Subscription.objects.get(student=request.user.student, course=wk.course)
        sub.quiz_count=sub.quiz_count+1
        sub.quiz_marks = sub.calculate_marks(count, question_count)
        if count>(q.count()/2):
            if sub.progress==wk:
                if sub.progress.final:
                    sub.completed=True
                    sub.complete_date=datetime.date.today()
                    sub.save()
                else:
                    sub.progress=sub.next_unit
                    sub.quiz_approve=False
                    sub.save()
            return HttpResponse("<h1 class='text-center'>Congratulations</h1><br><p>You have passed with score "+ str(count) + ".</p> Go <a href="+reverse('study',kwargs={'id':wk.course.id})+">back</a>")
        else:
            if sub.progress==wk:
                sub.quiz_approve=False
                sub.save()
            return HttpResponse("<h1 class='text-center'>Sorry</h1><br><p>You didn't pass. Your score is "+ str(count) + ".</p> Go <a href="+reverse('study',kwargs={'id':wk.course.id})+">back</a> and try again.")
    
    context = {
        'questions':q,
        'week':wk
    }
    return render(request, 'student/quiz.html', context)

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('student/certificate.html')
        context = {
            "student": request.user.student,
            "completed": request.user.student.completed_courses(),
        }
        html = template.render(context)
        pdf = render_to_pdf('student/certificate.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "certificate.pdf"
            content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

def view_teacher(request, username):
    t = models.Teacher.objects.get(user__username=username)
    c = models.Course.objects.filter(uploaded_by=t)
    context={
        'teacher':t,
        'courses':c,
    }
    return render(request, 'view_teacher.html', context)