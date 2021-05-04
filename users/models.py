from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.deletion import PROTECT
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from service.models import Organization, Service
from .managers import CustomUserManager
from location.models import Object
from PIL import Image

class Account(models.Model):
    account = models.CharField(unique=True, max_length=50, null=False, blank=False,verbose_name = "Счет")
    name = models.CharField(max_length=255, null=False, blank=False,verbose_name = "ФИО")
    object = models.ForeignKey(Object, on_delete=PROTECT, null=False, blank=False,verbose_name = "Объект", 
                                    related_name="object_accounts")
    total_square = models.FloatField(null=True, blank=True,verbose_name = "Общая плащадь")
    living_square = models.FloatField(null=True, blank=True,verbose_name = "Жилая площадь")
    share = models.FloatField(null=True, blank=True,verbose_name = "Доля")

    def __str__(self):
        return self.account
    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
    image = models.ImageField(null=True, upload_to='users/%Y/%m/%d/',)
    email = models.EmailField(unique=True, verbose_name="Эл. почта")
    username = models.CharField(unique=True,max_length=255,null=False, blank=False, verbose_name="Логин")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_number = PhoneNumberField(blank=False, null=False, verbose_name="Телефон")
    role = models.CharField(max_length=20,null=False, default="administrator",blank=False)
    specialization = models.ManyToManyField(Service, verbose_name="Обязанности")
    organization = models.ManyToManyField(Organization,  verbose_name="Организации")
    object = models.ManyToManyField(Object, verbose_name="Объекты", related_name="object_moderators")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользаватель"
        verbose_name_plural = "Пользавательи"

class Worker(CustomUser):
    class Meta:
        proxy = True
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

class Client(CustomUser):
    class Meta:
        proxy = True
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
      
class Administrator(CustomUser):
    class Meta:
        proxy = True
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

class Moderator(CustomUser):
    class Meta:
        proxy = True
        verbose_name = "Модератор"
        verbose_name_plural = "Модераторы"

class ClientAccount(models.Model):
    client = models.ForeignKey(CustomUser,on_delete=PROTECT, null=False, blank=False, related_name="client_accounts")
    account = models.ForeignKey(Account,on_delete=PROTECT, null=False, blank=False, related_name="account_clients")

    def __str__(self):
        return str(self.account)
        
    def address(self):
        return str(self.account.object.street.city.country)+", г. "+str(self.account.object.street.city)\
                            +", "+str(self.account.object.street)+", д. "+str(self.account.object.home[:-2])\
                                +", кв. "+str(self.account.object.appartment)
    class Meta:
        verbose_name = "Лицевой счет"
        verbose_name_plural = "Лицевой счеты"

class OrganizationWorker(models.Model):
    organization = models.ForeignKey(Organization, on_delete=PROTECT, null=False, blank=False, 
                                        related_name="organization_workers",verbose_name="Организацияs")
    worker = models.ForeignKey(Worker, on_delete=PROTECT, null=False, blank=False, 
                                        related_name="worker_organizations",verbose_name="Сотрудник")
        
    def __str__(self):
        return str(self.worker)
    class Meta:
        unique_together = ['organization', 'worker']
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
