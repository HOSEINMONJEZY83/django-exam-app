from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Exam , User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat password'
        })

        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'start_time', 'end_time', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exam', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        if user:
            self.fields['exam'].queryset = Exam.objects.filter(creator=user)
