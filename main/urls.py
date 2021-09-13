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
    

    
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)