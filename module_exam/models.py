from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Exam(models.Model):
    title = models.CharField(max_length=100)
    statr_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField()
    
    def __str__(self):
        return self.title
    
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=1) # a or b or c or d
    
    def __str__(self):
        return self.text[:50]
    
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected = models.CharField(max_length=1)
    submitted_at = models.DateTimeField(auto_now_add=True)