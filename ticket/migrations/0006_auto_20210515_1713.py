# Generated by Django 3.2 on 2021-05-15 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_auto_20210515_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.IntegerField(choices=[(1, 'На рассмотрении'), (3, 'Принято к исполнению'), (3, 'Выполнено')], default=1, max_length=255),
        ),
        migrations.AlterField(
            model_name='ticketstatushistory',
            name='status',
            field=models.IntegerField(choices=[(1, 'На рассмотрении'), (3, 'Принято к исполнению'), (3, 'Выполнено')], max_length=255),
        ),
    ]
