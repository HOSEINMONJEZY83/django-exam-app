from django.urls import path
from . import views

urlpatterns = [
    path('exam/<int:exam_id>/', views.take_exam, name='take_exam'),
]