# Generated by Django 3.2 on 2021-04-28 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20210418_1548'),
        ('users', '0020_auto_20210428_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),

    ]
