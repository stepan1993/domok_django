# Generated by Django 3.2 on 2021-06-08 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0005_alter_object_floor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='floor',
            field=models.IntegerField(blank=True, null=True, verbose_name='Этажей'),
        ),
    ]
