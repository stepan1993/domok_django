# Generated by Django 3.2 on 2021-04-18 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20210418_1548'),
        ('users', '0007_auto_20210418_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account',
            field=models.CharField(max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
