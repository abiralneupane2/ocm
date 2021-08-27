from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('browse/', views.browse, name='browse'),
    path('course/<str:code>/', views.course, name='course_details'),
    path('login/', views.userlogin, name='login'),
    path('university/<str:name>/', views.university, name='uni_details'),
    path('study/<str:code>/', views.study, name='study'),
]
