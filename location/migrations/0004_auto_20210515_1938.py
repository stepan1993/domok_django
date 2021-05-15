# Generated by Django 3.2 on 2021-05-15 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_auto_20210512_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('country', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='object',
            unique_together={('street', 'home', 'campus', 'floor', 'entrance', 'appartment')},
        ),
        migrations.AlterUniqueTogether(
            name='street',
            unique_together={('city', 'name')},
        ),
    ]