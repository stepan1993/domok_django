# Generated by Django 3.2 on 2021-04-28 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20210418_1548'),
        ('users', '0018_auto_20210428_2039'),
    ]

    operations = [

        migrations.DeleteModel(
            name='ModeratorObject',
        ),
    ]
