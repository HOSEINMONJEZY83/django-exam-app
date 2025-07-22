from django.shortcuts import render , get_object_or_404 ,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test
from .models import Exam, Question, Answer
import openpyxl
from django.http import HttpResponse , HttpResponseForbidden
from django.utils import timezone
from django.contrib.auth import authenticate, login , logout
from .forms import QuestionForm ,CustomUserCreationForm ,ExamForm

def home(request):
    now = timezone.now()
    
    if request.user.is_authenticated:
        if request.user.role == 'student':
            exams = Exam.objects.filter(
                is_active=True,
                start_time__lte=now,
                end_time__gte=now,
                creator__in=request.user.teachers.all()
            )
        elif request.user.role == 'teacher':
            exams = Exam.objects.filter(
                is_active=True,
                start_time__lte=now,
                end_time__gte=now,
                creator=request.user
            )
        else:
            exams = Exam.objects.none()
    else:
        exams = Exam.objects.none()

    return render(request, 'home.html', {'exams': exams})

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.user.role == 'teacher':
        return HttpResponseForbidden("Teachers are not allowed to take exams.")

    if request.user.role == 'student':
        if exam.creator not in request.user.teachers.all():
            return HttpResponseForbidden("You are not allowed to take this test.")

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
    return redirect('home')

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
            user = form.save(commit=False)
            user.save()
            if user.role == 'student':
                user.teachers.set(form.cleaned_data['teachers'])
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
@user_passes_test(is_teacher)
def export_excel(request):
    user = request.user
    exams = Exam.objects.filter(creator=user)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Exam Responses"

    headers = ['Exam Title', 'Student', 'Question', 'Selected Answer', 'Correct Answer']
    ws.append(headers)

    answers = Answer.objects.filter(question__exam__in=exams).select_related('question', 'user')

    for ans in answers:
        ws.append([
            ans.question.exam.title,
            ans.user.username,
            ans.question.text,
            ans.selected.upper(),
            ans.question.correct_answer.upper(),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=exam_responses.xlsx'

    wb.save(response)
    return response
