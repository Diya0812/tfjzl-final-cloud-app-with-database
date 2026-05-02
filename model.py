from django.db import models
from django.contrib.auth.models import User

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


# Lesson Model
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Question Model
class Question(models.Model):
    question_text = models.CharField(max_length=500)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


# Choice Model
class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


# Submission Model
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user}"
from django.contrib.auth.models import User

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user.username}"
