# Generated by Django 3.2 on 2021-05-10 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_auto_20210509_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.IntegerField(choices=[('1', 'Активный'), ('0', 'Новый'), ('-1', 'Блокирован')], default=1),
        ),
    ]
