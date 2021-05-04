# Generated by Django 3.2 on 2021-04-18 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20210418_1548'),
        ('service', '0002_auto_20210418_1548'),
        ('users', '0008_auto_20210418_1550'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Счет', 'verbose_name_plural': 'Счета'},
        ),

        migrations.AlterField(
            model_name='account',
            name='account',
            field=models.CharField(max_length=50, unique=True, verbose_name='Счет'),
        ),
        migrations.AlterField(
            model_name='account',
            name='living_square',
            field=models.FloatField(blank=True, null=True, verbose_name='Жилая площадь'),
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=255, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='account',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='location.object', verbose_name='Объект'),
        ),
        migrations.AlterField(
            model_name='account',
            name='share',
            field=models.FloatField(blank=True, null=True, verbose_name='Доля'),
        ),
        migrations.AlterField(
            model_name='account',
            name='total_square',
            field=models.FloatField(blank=True, null=True, verbose_name='Общая плащадь'),
        ),
    ]
