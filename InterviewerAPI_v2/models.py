from django.db import models
from django.contrib.auth import get_user_model


app_name = 'InterviewerAPI_v2'


class Interview(models.Model):
    name = models.CharField(max_length=100, help_text='Name of each interview')
    start_time = models.DateTimeField(help_text='Time when interview starts')
    end_time = models.DateTimeField(help_text='Time when interview ends')
    description = models.TextField(max_length=500, null=True, help_text='Interview description')

    def __str__(self):
        return self.name


class Question(models.Model):
    TEXT_ANSWER = 'TA'
    ONE_ANSWER = 'OA'
    MANY_ANSWER = 'MA'
    TYPE_ANSWER_CHOICES = [
        (TEXT_ANSWER, 'Text answer'),
        (ONE_ANSWER, 'One answer'),
        (MANY_ANSWER, 'Many answers'),
    ]

    interview = models.ForeignKey(Interview, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(max_length=500, help_text='Question text')
    type = models.CharField(max_length=2, choices=TYPE_ANSWER_CHOICES, default=TEXT_ANSWER, help_text='Question type')

    def __str__(self):
        return self.text


class PossibleAnswer(models.Model):
    question = models.ForeignKey(Question, related_name='possible_answers', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(get_user_model(), null=True,  on_delete=models.CASCADE, help_text='Token of user')
    interview = models.ForeignKey(Interview, on_delete=models.SET('deleted'))
    question = models.ForeignKey(Question, on_delete=models.SET('deleted'))
    answer = models.ManyToManyField(PossibleAnswer, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{} : {}'.format(self.user, self.interview)
