from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login',views.custom_login, name='login'),
    path('logout',views.user_logout, name='logout'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('exam/<int:exam_id>/', views.take_exam, name='take_exam'),
]