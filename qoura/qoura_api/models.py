from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(unique=True, max_length=130)
    url_title = models.CharField(unique=True, max_length=130, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    answer = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('author', 'question',)

    def __str__(self):
        return self.answer

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='like')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    like = models.BooleanField()

    class Meta:
        unique_together = ('liker', 'answer',)
    