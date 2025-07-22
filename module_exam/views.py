from django.shortcuts import render , get_object_or_404 ,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test
from .models import Exam, Question, Answer
from django.utils import timezone
from django.contrib.auth import authenticate, login , logout
from .forms import QuestionForm ,CustomUserCreationForm ,ExamForm

def home(request):
    now = timezone.now()
    exams = Exam.objects.filter(is_active=True, start_time__lte=now, end_time__gte=now)
    return render(request, 'home.html', {'exams': exams})

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    answered = Answer.objects.filter(user=request.user, question__exam=exam).exists()
    if answered:
        return render(request, 'already_taken.html')

    if not exam.is_active or not (exam.start_time <= timezone.now() <= exam.end_time):
        return render(request, 'not_available.html')

    questions = Question.objects.filter(exam=exam)

    if request.method == "POST":
        correct = 0
        results = []
        for question in questions:
            selected = request.POST.get(f"question_{question.id}")
            if selected:
                Answer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'selected': selected}
                )
                is_correct = selected == question.correct_answer
                if is_correct:
                    correct += 1

                results.append({
                    'question': question,
                    'selected': selected,
                    'is_correct': is_correct,
                    'correct_answer': question.correct_answer,
                })

        score = round((correct / questions.count()) * 100)
        context = {
            'score': score,
            'results': results,
        }
        return render(request, 'resualt.html', context)
    
    context = {
        'exam': exam,
        'questions': questions,
    }
    return render(request, 'take_exam.html', context)

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_superuser:
                messages.error(request, "Invalid username or password.")
                return render(request, 'login.html')
            login(request, user)
            if user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    if request.method == 'POST':
        if 'create_exam' in request.POST:
            exam_form = ExamForm(request.POST)
            if exam_form.is_valid():
                exam = exam_form.save(commit=False)
                exam.creator = request.user
                exam.save()
                return redirect('teacher_dashboard')
            question_form = QuestionForm(user=request.user)
        elif 'create_question' in request.POST:
            question_form = QuestionForm(request.POST, user=request.user)
            if question_form.is_valid():
                question_form.save()
                return redirect('teacher_dashboard')
            exam_form = ExamForm()
    else:
        exam_form = ExamForm(initial={
            'start_time': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'end_time': (timezone.now() + timezone.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'is_active': True,
        })
        question_form = QuestionForm(user=request.user)

    questions = Question.objects.filter(exam__creator=request.user)

    context = {
        'exam_form': exam_form,
        'question_form': question_form,
        'questions': questions,
    }
    return render(request, 'teacher_dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

