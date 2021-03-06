# Generated by Django 3.2 on 2021-04-29 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20210418_1548'),
        ('users', '0021_auto_20210428_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(null=True, upload_to='users/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='organizationworker',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='organization_workers', to='service.organization', verbose_name='Организацияs'),
        ),
    ]
