from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .user_manager import CustomUserManager


class QuestionModel(models.Model):
    CHOICES = (
        ('TXT', 'Ответ текстом'),
        ('ONE', 'Выбор одного правильного варианта'),
        ('MANY', 'Выбор нескольких правильных вариантов'),
    )
    text = models.TextField(blank=False, null=False)
    type = models.CharField(max_length=50, choices=CHOICES)


class AnswerModel(models.Model):
    text = models.TextField(blank=False, null=False)
    question = models.OneToOneField(QuestionModel,
                                    on_delete=models.CASCADE)


class PollModel(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False, null=False)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(blank=False, null=False)
    questions = models.ManyToManyField(QuestionModel, blank=True)


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True)
    anon_id = models.IntegerField(null=True, default=None)
    polls = models.ManyToManyField(PollModel, blank=True)
    answers = models.ManyToManyField(AnswerModel, blank=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
