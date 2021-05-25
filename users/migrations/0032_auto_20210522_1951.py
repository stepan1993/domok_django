# Generated by Django 3.2 on 2021-05-22 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_faktura'),
    ]

    operations = [
        migrations.AddField(
            model_name='faktura',
            name='account',
            field=models.CharField( max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.IntegerField(choices=[(1, 'Активный'), (0, 'Новый'), (-1, 'Блокирован')], default=1, verbose_name='Статус'),
        ),
    ]
