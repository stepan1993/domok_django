# Generated by Django 3.2 on 2021-05-04 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20210418_1548'),
        ('news', '0004_rename_objects_news_news_objects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_objects',
            field=models.ManyToManyField(blank=True, null=True, to='location.Object'),
        ),
    ]
