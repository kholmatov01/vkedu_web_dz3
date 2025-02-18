from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='bred')
    avatar = models.ImageField(blank=True, null=True)
    def __str__(self):
        return self.username.username

class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.tag

class QuestionManager(models.Manager):
    def get_hot(self):
        return self.annotate(likes_count=Count('questionlike')).order_by('-likes_count')
    def get_new(self):
        return self.annotate(likes_count=Count('questionlike')).order_by('-created_at')
    def get_with_tag(self, tag_p):
        return self.filter(tags__exact=tag_p).annotate(likes_count=Count('questionlike')).order_by('-likes_count')
    def get_with_title(self, title_p):
        return self.filter(title__exact=title_p).annotate(likes_count=Count('questionlike')).order_by('-likes_count')
    def get_with_id(self, id):
        return self.filter(id__exact=id).annotate(likes_count=Count('questionlike')).get(id__exact=id)
    

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('s', 'Solved'),
        ('ns', 'Not Solved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ns')
    tags = models.ManyToManyField(Tag)
    objects = QuestionManager()
    def __str__(self):
        return self.title + ' (' + self.user.username + ')'

class AnswerManager(models.Manager):
    def get_with_question(self, question_p):
        return self.filter(question__exact=question_p).annotate(likes_count=Count('answerlike')).order_by('-likes_count')
    
class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    correct = models.BooleanField(default=False)
    objects = AnswerManager()
    def __str__(self):
        return self.user.username + '(' + self.question.title + ')'
    

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + '+' + self.question.title
    class Meta:
        unique_together = ("question", "user")

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + '+' + self.answer.user.username
    class Meta:
        unique_together = ("answer", "user")
