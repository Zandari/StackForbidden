from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from typing import Optional


class QuestionManager(models.Manager):
    def get_hot(self):
        return (self
                .all()
                .annotate(votes_num=models.Count('vote'))
                .order_by('-votes_num'))


    def get_new(self):
        return (self
                .all()
                .order_by('created_at'))


class TagManager(models.Manager):
    def get_popular(self):
        return (self
                .all()
                .annotate(questions_num=models.Count('questions'))
                .order_by('-questions_num'))


class ProfileManager(models.Manager):
    def get_best(self):
        return (self
                .all()
                .annotate(activity=models.Count('question')+models.Count('answer'))
                .order_by('-activity'))


class Profile(models.Model):
    objects = ProfileManager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="uploads", default="placeholder.png")


class Tag(models.Model):
    objects = TagManager()

    name = models.CharField(max_length=20, unique=True)


class Question(models.Model):
    objects = QuestionManager()

    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="questions")
    created_at = models.DateTimeField()


class Answer(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField()

class Vote(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="votes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="votes", null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="votes", null=True)
    is_positive = models.BooleanField(help_text="Describes is record upvote or downvote")
    created_at = models.DateTimeField()

    def clean(self, *args, **kwargs):
        if self.question is not None and self.answer is not None:
            raise ValidationError("Only one of the fields should be filled")
        elif self.question is None and self.answer is None:
            raise ValidationError("One of the fields should be filled")
        
        return super().clean(*args, **kwargs)