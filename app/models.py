from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from typing import Optional


class QuestionManager(models.Manager):
    def get_hot(self):
        return (self
                .all()
                .annotate(votes_num=models.Count('votes'))
                .order_by('-votes_num'))

    def get_new(self):
        return self.all().order_by('-created_at')


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
                .annotate(activity=models.Count('questions')+models.Count('answers'))
                .order_by('-activity'))


class Profile(models.Model):
    objects = ProfileManager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="uploads", default="placeholder.png")

    @property
    def answers_count(self) -> int:
        return len(self.answers.all())


class Tag(models.Model):
    objects = TagManager()

    name = models.CharField(max_length=20, unique=True)


class Question(models.Model):
    objects = QuestionManager()

    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="questions")
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="questions")
    created_at = models.DateTimeField()

    @property
    def votes_count(self) -> int:
        related_votes = self.question_votes.all()
        positive = related_votes.filter(is_positive=True).count()
        total = related_votes.count()
        return -total + positive * 2

    @property
    def answers_count(self) -> int:
        return len(self.answers.all())


class Answer(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    is_correct = models.BooleanField(default=False)
    text = models.TextField()
    created_at = models.DateTimeField()

    @property
    def votes_count(self):
        return len(self.answer_votes.all())


class AnswerVote(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="answer_votes")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answer_votes", null=True)
    is_positive = models.BooleanField(help_text="Describes is record upvote or downvote")
    created_at = models.DateTimeField()


class QuestionVote(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="question_votes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_votes", null=True)
    is_positive = models.BooleanField(help_text="Describes is record upvote or downvote")
    created_at = models.DateTimeField()