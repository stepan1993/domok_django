from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

class Country(models.Model):
    name = models.CharField(max_length=255,null=False, blank=False,verbose_name="Название", unique=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ["name"]
        verbose_name_plural = '    Страны'
        verbose_name = '    Страна'


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=PROTECT, null=False, blank=False, related_name="cities",verbose_name="Страна")
    name = models.CharField(max_length=255,null=False, blank=False,verbose_name="Название")

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ['country', 'name']
        ordering = ["name",]
        verbose_name_plural = "   Города"
        verbose_name = "   Город"


class Street(models.Model):
    city = models.ForeignKey(City, on_delete=PROTECT, null=False, blank=False, 
                            related_name="city_streets",verbose_name="Город")
    name = models.CharField(max_length=255,null=False, blank=False,verbose_name="Название")
    
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ['city', 'name']
        ordering = ["name",]
        verbose_name_plural = "  Улицы"
        verbose_name = "  Улица"

class Object(models.Model):
    street = models.ForeignKey(Street, on_delete=PROTECT, null=False, blank=False, 
                                    related_name="street_objects",verbose_name="Улица")
    home = models.CharField(max_length=255,null=False, blank=False,verbose_name="Дом")
    campus = models.CharField(max_length=255,null=True, blank=True,verbose_name="Корпус")
    floor = models.IntegerField(null=True, blank=True,verbose_name="Этажей")
    entrance_number = models.CharField(null=True, blank=True,max_length=255,verbose_name="Подъездов")
    appartment_number = models.CharField(null=True, blank=True,max_length=255,verbose_name="Квартир")
    comment = models.TextField(null=True, blank=True,verbose_name="Описание")

    def __str__(self):
        text = f"{self.street.city.country}, {self.street.city}, {self.street}, {self.home}, "
        if self.campus is not None and self.campus !=0:
            text+= "корп. "+str(self.campus)  
        else:
            text+= ""
        text+=" кв. "+str(self.appartment_number)
        return text
    class Meta:
        unique_together = ['street', 'home','campus','floor','entrance_number','appartment_number']
        verbose_name_plural = " Объекты"
        verbose_name = " Объект"
