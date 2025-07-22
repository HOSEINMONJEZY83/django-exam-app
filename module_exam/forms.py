from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Exam , User


class CustomUserCreationForm(UserCreationForm):
    teachers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='teacher'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label='Select Teachers'
    )

    class Meta:
        model = User
        fields = ['username', 'role', 'teachers', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repeat password'})
        self.fields['teachers'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        teachers = cleaned_data.get('teachers')
        if role == 'student' and not teachers:
            raise forms.ValidationError('Students must select at least one teacher.')
        return cleaned_data
        

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
