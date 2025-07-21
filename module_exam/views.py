from django.shortcuts import render , get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Answer
from django.utils import timezone

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
