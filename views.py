from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Choice, Submission


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    enrollment = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).first()

    submission = Submission.objects.create(enrollment=enrollment)

    selected_choice_ids = request.POST.getlist('choice')
    for choice_id in selected_choice_ids:
        choice = Choice.objects.get(pk=choice_id)
        submission.choices.add(choice)

    submission.save()

    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course_id, submission.id))
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    selected_choices = submission.choices.all()
    selected_ids = [choice.id for choice in selected_choices]

    total_score = 0
    possible_score = 0

    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': total_score,
        'possible': possible_score,
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
