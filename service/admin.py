from location.models import City, Country, Object, Street
from django.contrib import admin
from .models import Organization, OrganizationObject, OrganizationService, Service
from django_cascading_dropdown_widget.widgets import DjangoCascadingDropdownWidget
from django_cascading_dropdown_widget.widgets import CascadingModelchoices
from django import forms
from users.models import CustomUser, OrganizationWorker

class OrganizationObjectForm(forms.ModelForm):
    class Meta:
        model = OrganizationObject
        exclude = []
        widgets = {
            "object": DjangoCascadingDropdownWidget(choices=CascadingModelchoices({
                "model": Country,
                "related_name": "cities",
            },{
                "model": City,
                "related_name": "city_streets",
                "fk_name":"country"
            },{
                "model": Street,
                "related_name": "street_objects",
                "fk_name":"city"
            },{
                "model": Object,
                "fk_name": "street",
            })),
        }

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'nominative','genitive','dative')
    search_fields = ['name', 'nominative','genitive','dative']

class OrganizationWorkerAdmin(admin.TabularInline):
    extra = 1
    model = OrganizationWorker
    raw_id_fields = ('worker',)
    fields = ['worker','email','phone_number','status']
    readonly_fields =['email','phone_number','status']
    def email(self,obj):
        return obj.worker.email
    def phone_number(self,obj):
        return obj.worker.phone_number
    def status(self,obj):
        return obj.worker.is_active
    email.short_description="Эл. Почта"
    phone_number.short_description="Телефон"
    status.short_description="Статус"
    
class OrganizationServiceInline(admin.TabularInline):
    model = OrganizationService
    extra=0

class OrganizationObjectInline(admin.TabularInline):
    model = OrganizationObject
    list_display = ('country', 'city','street','object')
    extra=0
    form = OrganizationObjectForm

@admin.register(Organization)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn','description')
    search_fields = ('name', 'inn','description')
    inlines = [
            OrganizationServiceInline,
            OrganizationObjectInline,
            OrganizationWorkerAdmin
        ]
