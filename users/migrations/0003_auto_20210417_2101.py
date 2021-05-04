# Generated by Django 3.2 on 2021-04-17 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210417_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
            ],
            options={
                'verbose_name': 'worker',
                'verbose_name_plural': 'workers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.customuser',),
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(default='administrator', max_length=20),
        ),
    ]
