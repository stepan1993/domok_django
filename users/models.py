from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from service.models import Organization, Service
from .managers import CustomUserManager
from location.models import Object

ACTIVE_STATUS = [
        (1, 'Активный'),
        (0, 'Новый'),
        (-1, 'Блокирован'),
    ]
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Отчество")
    image = models.ImageField(null=True, upload_to='users/%Y/%m/%d/',)
    email = models.EmailField(verbose_name="Эл. почта")
    username = models.CharField(unique=True,max_length=255,null=False, blank=False, verbose_name="Логин")
    is_staff = models.BooleanField(default=False)
    is_active = models.IntegerField(default=1, choices=ACTIVE_STATUS)
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

class Account(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=SET_NULL, null=True, 
                                                blank=True, related_name="custom_user_account")
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
