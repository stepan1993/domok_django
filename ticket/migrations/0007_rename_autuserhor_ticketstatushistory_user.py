# Generated by Django 3.2 on 2021-05-15 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_auto_20210515_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketstatushistory',
            old_name='autuserhor',
            new_name='user',
        ),
    ]
