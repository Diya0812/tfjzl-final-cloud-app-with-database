from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Course, Question, Choice, Submission
from django.contrib.auth.decorators import login_required


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        selected_choices = request.POST.getlist('choice')

        submission = Submission.objects.create(user=request.user)

        for choice_id in selected_choices:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)

        submission.save()

        return HttpResponseRedirect(f'/result/{submission.id}/')


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    choices = submission.choices.all()

    total = choices.count()
    correct = choices.filter(is_correct=True).count()

    score = 0
    if total > 0:
        score = (correct / total) * 100

    context = {
        'submission': submission,
        'choices': choices,
        'score': score,
        'correct': correct,
        'total': total,
    }

    return render(request, 'exam_result.html', context)
