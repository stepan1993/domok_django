from django.db import models
from django.db.models.deletion import PROTECT
from phonenumber_field.modelfields import PhoneNumberField
from location.models import Object

class Service(models.Model):
    name = models.CharField(max_length=255,null=False, blank=False,verbose_name="Название")
    nominative = models.CharField(max_length=255,null=False, blank=False,verbose_name="Именительный падеж")
    genitive = models.CharField(max_length=255,null=False, blank=False,verbose_name="Родительный падеж")
    dative = models.CharField(max_length=255,null=False, blank=False,verbose_name="Дательный падеж")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="Услуги"
        verbose_name="Услуга"

class Organization(models.Model):
    name = models.CharField(max_length=255,null=False, blank=False,verbose_name="Название")
    inn = models.CharField(max_length=255,null=True, blank=True,verbose_name="ИНН")
    description = models.TextField(null=True, blank=True,verbose_name="Описание")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="Организации"
        verbose_name="Организация"

class OrganizationService(models.Model):
    organization = models.ForeignKey(Organization, on_delete=PROTECT, null=False, blank=False, 
                                related_name="organization_services")
    service = models.ForeignKey(Service, on_delete=PROTECT, null=False, blank=False, 
                                related_name="service_organizations",verbose_name="Услуга")
    contact_phone = PhoneNumberField(blank=False, null=False,verbose_name="Контактный телефон")
    contact_email = models.EmailField(max_length=254,null=False, blank=False,verbose_name="Контактный Эл. почта") 
    
    class Meta:
        unique_together = ['organization', 'service']
        verbose_name_plural="Услуги"
        verbose_name="Услуга"

class OrganizationObject(models.Model):
    organization = models.ForeignKey(Organization, on_delete=PROTECT, null=False, blank=False, 
                                        related_name="organization_objects")
    object = models.ForeignKey(Object, on_delete=PROTECT, null=False, blank=False, 
                                        related_name="object_organization",verbose_name="Объект")
        
    def __str__(self):
        return str(self.object)
    class Meta:
        unique_together = ['organization', 'object']
        verbose_name_plural="Объекты"
        verbose_name="Объект"

