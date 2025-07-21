from django.shortcuts import render , get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Answer
from django.utils import timezone

# Create your views here.
@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if not exam.is_active or not (exam.start_time <= timezone.now() <= exam.end_time):
        return render(request, 'exam/not_available.html')
    questions = Question.objects.filter(exam=exam)
    if request.method == "POST":
        correct = 0
        for question in questions:
            selected = request.POST.get(f"question_{question.id}")
            if selected:
                Answer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'selected': selected}
                )
                if selected == question.correct_answer:
                    correct += 1

        score = round((correct / questions.count()) * 100)
        return render(request, 'exam/result.html', {'score': score})

    return render(request, 'exam/take_exam.html', {
        'exam': exam,
        'questions': questions,
    })