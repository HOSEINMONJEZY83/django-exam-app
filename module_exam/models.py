from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    teachers = models.ManyToManyField('self', symmetrical=False, limit_choices_to={'role': 'teacher'}, blank=True)


class Exam(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=150)
    option_b = models.CharField(max_length=150)
    option_c = models.CharField(max_length=150)
    option_d = models.CharField(max_length=150)
    correct_answer = models.CharField(max_length=1,choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])
    
    def __str__(self):
        return self.text[:50]
    
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected = models.CharField(max_length=1,choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')
        
    def __str__(self):
        return f"{self.user.username} - {self.question.id} - {self.selected}"