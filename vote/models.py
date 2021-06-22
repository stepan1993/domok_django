from django.db.models.expressions import Subquery
from location.models import Object
from django.db.models.deletion import CASCADE, PROTECT
from users.models import CustomUser
import datetime
from django.db import models
from django.db.models import Count, Max, Sum
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
class Vote(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('finished', 'Завершен')
    ]
    object = models.ForeignKey(Object, on_delete=CASCADE, related_name="object_votes",null=True, blank=True)
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

    @property
    def is_past_due(self):
        return self.end_date < datetime.date.today()

    @property
    def is_future_due(self):
        return self.start_date > datetime.date.today()

    @property
    def is_active(self):
        return self.start_date <= datetime.date.today() and self.end_date>=datetime.date.today()

    @property
    def for_sum(self):
        try:
            if self.vote_type=="account":
                return round(self.vote_members.filter(point=1).count()*100/self.vote_members.all().count())
            else:
                item = self.vote_members.filter(point=1)
                result = 0
                for i in item:
                    user_account = self.object.object_accounts.get(custom_user_id=i.member.id)
                    result+=user_account.share*100
                return round(result,2)
        except:
            return 0

    @property
    def against_sum(self):
        try:
            if self.vote_type=="account":
                return round(self.vote_members.filter(point=2).count()*100/self.vote_members.all().count())
            else:
                item = self.vote_members.filter(point=2)
                result = 0
                for i in item:
                    user_account = self.object.object_accounts.get(custom_user_id=i.member.id)
                    result+=user_account.share*100
                return round(result,2)
        except:
            return 0
    
    @property
    def abstain_sum(self):
        try:
            if self.vote_type=="account":
                return round(self.vote_members.filter(point=3).count()*100/self.vote_members.all().count())
            else:
                item = self.vote_members.filter(point=3)
                result = 0
                for i in item:
                    user_account = self.object.object_accounts.get(custom_user_id=i.member.id)
                    result+=user_account.share*100
                return round(result,2)
        except:
            return 0

    @property
    def for_sum_square(self):
        item = self.vote_members.filter(point=1)
        result = 0
        for i in item:
            user_account = self.object.object_accounts.get(custom_user_id=i.member.id)
            result+=user_account.total_square*user_account.share
        return round(result,2)
            
    @property
    def against_sum_square(self):
        item = self.vote_members.filter(point=2)
        result = 0
        for i in item:
            user_account = self.object.object_accounts.get(custom_user_id=i.member.id)
            result+=user_account.total_square*user_account.share
        return round(result,2)
    
    @property
    def abstain_sum_square(self):
        item = self.vote_members.filter(point=3)
        result = 0
        for i in item:
            user_account = self.object.object_accounts.get(custom_user_id=i.member.id)
            result+=user_account.total_square*user_account.share
        return round(result,2)

    @property
    def members_count(self):
        return self.vote_members.all().count()

    @property
    def members_count_percentage(self):
        try:
            if self.vote_type=="account":
                return round(self.vote_members.all().count()*100/self.object.object_accounts.all().count(),2)
            else:
                item = self.vote_members.all()
                result = 0
                for i in item:
                    user_account = self.object.object_accounts.get(custom_user_id=i.member.id)
                    result+=user_account.share*100
                return round(result,2)
        except:
            return 0
    
    @property
    def highest_vote(self):
        return self.vote_members.all().order_by('point').values('point').annotate(
                point_count=Count('point')).aggregate(maxval=Max('point_count'))['maxval']

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
    
    @property
    def user_vote(self):
        user_account = self.vote.object.object_accounts.get(custom_user_id=self.member.id)
        return user_account.share*100

    @property
    def user_total_square(self):
        return self.vote.object.object_accounts.get(custom_user_id=self.member.id).total_square
    @property
    def user_appartment_number(self):
        return self.vote.object.object_accounts.get(custom_user_id=self.member.id).object.appartment_number
