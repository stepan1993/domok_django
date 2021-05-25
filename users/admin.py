
from django.contrib import admin
from .models import Account, Administrator, Client,  Moderator, Worker, Faktura
from django.utils.html import format_html

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
        list_display = ('account', 'user_full_name','share','address')
        # list_display_links = ['account','address']
        def user_full_name(self,obj):
                return f"{obj.custom_user.last_name} {obj.custom_user.first_name} {obj.custom_user.middle_name} "
        def address(self,obj):
                return f"{obj.object}"
        user_full_name.short_description="ФИО"
        address.short_description="Адрес"

@admin.register(Faktura)
class Faktura(admin.ModelAdmin):
        change_list_template = 'accounts/change_list.html'
        list_display = ('account_name', 'year','month','download_button')
        readonly_fields = ['account_name',"created_at","created_by",'file_name']
        exclude = ["file"]
        list_per_page = 10
        
        def download_button(self, obj):
                return format_html('<span style="width:100%; display:flex; justify-content:flex-end">\
                        <a class="button"  href="/media/{}">Скачать</a>\
                        </span>', obj.file, obj.id)
        download_button.short_description=""
        
        def file_name(self, obj):
                return format_html('<a class="button"  href="/media/{}">Скачать</a>', obj.file)
        download_button.short_description=""
        file_name.short_description="Файл"