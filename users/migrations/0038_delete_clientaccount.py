# Generated by Django 3.2 on 2021-06-08 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_merge_20210605_1247'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClientAccount',
        ),
    ]
