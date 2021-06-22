from users.models import Account
from django.contrib import admin
from .models import Country, City, Street, Object
from django_cascading_dropdown_widget.widgets import DjangoCascadingDropdownWidget
from django_cascading_dropdown_widget.widgets import CascadingModelchoices
from django import forms
from django.utils.html import format_html

class StreetForm(forms.ModelForm):
    class Meta:
        model = Street
        exclude = []
        widgets = {
            "city": DjangoCascadingDropdownWidget(choices=CascadingModelchoices({
                "model": Country,
                "related_name": "cities",
            },{
                "model": City,
                "fk_name": "country",
            })),
        }

class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        exclude = []
        widgets = {
            "street": DjangoCascadingDropdownWidget(choices=CascadingModelchoices({
                "model": Country,
                "related_name": "cities",
            },{
                "model": City,
                "related_name": "city_streets",
                "fk_name":"country"
            },{
                "model": Street,
                "fk_name": "city",
            })),
        }

class ObjectAccount(admin.TabularInline):
    model = Account
    extra=0
    readonly_fields = ('account','name','total_square','living_square','share')
    can_delete = False
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fields = ('name', )
    list_display = ('name', 'city','street','object','change_button', 'delete_button')
    search_fields = ['name']
    def city(self,obj):
        return obj.cities.all().count()
    def street(self,obj):
        return Street.objects.filter(city__country=obj).count()
    def object(self,obj):
        return Object.objects.filter(street__city__country=obj).count()
    city.short_description="Городов"
    street.short_description="Улиц"
    object.short_description="Объектов"
    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/location/country/{}/change/">Change</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/location/country/{}/delete/">Delete</a>', obj.id)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    fields = ('country','name')
    list_display = ('name','country','street','object' )
    list_filter = ('country', )
    search_fields = ['country__name','name']

    def street(self,obj):
        return obj.city_streets.all().count()
    
    def object(self,obj):
        return Object.objects.filter(street__city=obj).count()
    street.short_description="Улиц"
    object.short_description="Объектов"

@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    fields = ('city','name')
    list_display = ('name','country','city','object' )
    list_filter = ('city__country','city',)
    search_fields = ['city__country__name','city__name','name']
    form = StreetForm
    def object(self,obj):
        return obj.street_objects.all().count()
    def country(self,obj):
        return obj.city.country
    country.short_description="Страна"
    object.short_description="Объектов"

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ['country','city',"street","home","campus","floor","entrance_number", "appartment_number"]
    list_filter = ('street__city__country','street__city','street',)
    search_fields = ['street__city__country__name','street__city__name','street__name']
    form = ObjectForm
    inlines = [ObjectAccount]
    def country(self,obj):
        return obj.street.city.country
    def city(self,obj):
        return obj.street.city

    country.short_description="Страна"
    city.short_description="Город"