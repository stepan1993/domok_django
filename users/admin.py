
from django.contrib import admin
from .models import Account, Administrator, Client,  Moderator, Worker


@admin.register(Client)
class Client(admin.ModelAdmin):
        fields = ('first_name', 'last_name','middle_name','email','phone_number','username','is_active')
        list_display = ('first_name', 'last_name','middle_name','email','phone_number','is_active')
        search_fields =['first_name', 'last_name','middle_name','email','phone_number']
        change_form_template = "users/change-form.html"
        # inlines = [AccountInline,]
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
