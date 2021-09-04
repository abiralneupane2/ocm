from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('browse/', views.browse, name='browse'),
    path('course/<str:code>/', views.course, name='course_details'),
    path('login/', views.userlogin, name='login'),
    path('university/<str:name>/', views.university, name='uni_details'),
    path('study/<str:code>/', views.study, name='study'),
    path('comment/', views.Comment.as_view(), name='comment'),
    path('quiz/<int:week_id>/', views.quiz, name='quiz'),
    path('register/', views.register, name='register'),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)