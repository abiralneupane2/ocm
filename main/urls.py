from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('browse/', views.browse, name='browse'),
    path('course/<str:id>/', views.course, name='course_details'),
    path('login/', views.userlogin, name='login'),
    path('study/<str:id>/', views.study, name='study'),
    path('comment/', views.Comment.as_view(), name='comment'),
    path('quiz/<int:week_id>/', views.quiz, name='quiz'),
    path('register/', views.register, name='register'),
    path('teacher_register/', views.teacher_register, name='teacher_register'),
    path('add_course/', views.add_course, name='add_course'),
    path('start_lesson/<int:week_id>', views.start_lesson, name='start_lesson'),
    path('edit_course/<int:id>', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/<int:user_id>/', views.quiz_approve, name='quiz_approve'),
    path('course/<int:course_id>/quiz/', views.manage_quiz, name='manage_quiz'),
    path('start_lesson/<int:week_id>/quiz', views.take_quiz, name = 'take_quiz'), 
    path('download',views.GeneratePDF.as_view(), name='download_certificate')  
    
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)