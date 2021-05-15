# Generated by Django 3.2 on 2021-05-15 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20210418_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='service',
            name='dative',
            field=models.CharField(max_length=255, unique=True, verbose_name='Дательный падеж'),
        ),
        migrations.AlterField(
            model_name='service',
            name='genitive',
            field=models.CharField(max_length=255, unique=True, verbose_name='Родительный падеж'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='service',
            name='nominative',
            field=models.CharField(max_length=255, unique=True, verbose_name='Именительный падеж'),
        ),
    ]
