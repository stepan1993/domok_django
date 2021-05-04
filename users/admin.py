from location.models import City, Country, Object, Street
from service.models import Service
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Administrator, Client, ClientAccount, CustomUser,  Moderator, Worker
from django import forms
from django_cascading_dropdown_widget.widgets import DjangoCascadingDropdownWidget
from django_cascading_dropdown_widget.widgets import CascadingModelchoices

class AccountInline(admin.TabularInline):
        model = ClientAccount
        raw_id_fields = ['account']
        fields = ['account','address']
        readonly_fields = ['address']
        extra=1


@admin.register(Client)
class Client(admin.ModelAdmin):
        fields = ('first_name', 'last_name','middle_name','email','phone_number','username','is_active')
        list_display = ('first_name', 'last_name','middle_name','email','phone_number','is_active')
        search_fields =['first_name', 'last_name','middle_name','email','phone_number']
        change_form_template = "users/change-form.html"
        inlines = [AccountInline,]
        def get_queryset(self, request):
                qs = super().get_queryset(request)
                return qs.filter(role="client")
        def save_model(self, request, obj, form, change):
                obj.role = "client"
                obj.save()

@admin.register(Administrator)
class Administrator(admin.ModelAdmin):
        fields = ('first_name', 'last_name','middle_name','email','phone_number','username','is_active')
        list_display = ('first_name', 'last_name','middle_name','email','phone_number','is_active')
        search_fields =['first_name', 'last_name','middle_name','email','phone_number']
        change_form_template = "users/change-form.html"
        def get_queryset(self, request):
                qs = super().get_queryset(request)
                return qs.filter(role="administrator")
        def save_model(self, request, obj, form, change):
                obj.role = "administrator"
                obj.is_staff = True
                obj.is_superuser =True
                obj.save()

@admin.register(Worker)
class Worker(admin.ModelAdmin):
        fields = ('first_name', 'last_name','middle_name','email','phone_number','username','specialization','organization','is_active')
        list_display = ('first_name', 'last_name','middle_name','email','phone_number','is_active')
        filter_horizontal =['specialization','organization']
        search_fields =['first_name', 'last_name','middle_name','email','phone_number']
        change_form_template = "users/change-form.html"

        def get_queryset(self, request):
                qs = super().get_queryset(request)
                return qs.filter(role="worker")
        def save_model(self, request, obj, form, change):
                obj.role = "worker"
                obj.save()

@admin.register(Moderator)
class Moderator(admin.ModelAdmin):
        fields = ('first_name', 'last_name','middle_name','email','phone_number','username','object','is_active')
        list_display = ('first_name', 'last_name','middle_name','email','phone_number','is_active')
        search_fields =['first_name', 'last_name','middle_name','email','phone_number']
        change_form_template = "users/change-form.html"
        filter_horizontal = ("object",)
        def get_queryset(self, request):
                qs = super().get_queryset(request)
                return qs.filter(role="moderator")
        def save_model(self, request, obj, form, change):
                obj.role = "moderator"
                obj.is_staff = True
                obj.save()

@admin.register(Account)
class Account(admin.ModelAdmin):
    change_list_template = 'users/change_list.html'
