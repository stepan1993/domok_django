from django.db.models.deletion import CASCADE, PROTECT
from users.models import CustomUser
from django.db import models

class Vote(models.Model):
    VOTE_TYPES = [
        ('share', 'Долями'),
        ('account', 'Голосами')
    ]
    QUORUM_CHOICES = [
        (50, ">50%"),
        (60, ">60%"),
        (70, ">70%"),
        (80, ">80%"),
        (90, ">90%"),
        (100, "100%"),
    ]
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('finished', 'Завершен')
    ]
    question = models.CharField(max_length=255, null=False, blank=False, verbose_name="Вопрос")
    description = models.TextField(verbose_name="Описание", null=True, blank=False)
    start_date = models.DateField(verbose_name="Начало", null=False, blank=False)
    end_date = models.DateField(verbose_name="Окончание", null=False, blank=False)
    vote_type = models.CharField(choices=VOTE_TYPES, max_length=255, default="share", null=False, blank=False, verbose_name="Тип голосования")
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default="active", null=False, blank=False, verbose_name="Статус")
    quorum = models.IntegerField(choices = QUORUM_CHOICES, default=50, null=False, blank=False, verbose_name="Кворум")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=PROTECT, null=False, blank=False, related_name="user_created_votes")
    
    class Meta:
        verbose_name_plural = 'Голосования'
        verbose_name = 'Голосования'


class VoteMember(models.Model):
    POINT_CHOICES = [
        (1, "ЗА"),
        (2, "ПРОТИВ"),
        (3, "ВСЕ РАВНО")
    ]
    member = models.ForeignKey(CustomUser, on_delete=PROTECT, related_name="user_votes",null=False, blank=False)
    vote = models.ForeignKey(Vote, related_name="vote_members", null=True, blank=True, on_delete=CASCADE)
    point = models.IntegerField(choices=POINT_CHOICES, default=1, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Участники'
        verbose_name = 'Участник'
