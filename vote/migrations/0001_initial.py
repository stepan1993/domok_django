# Generated by Django 3.2 on 2021-04-29 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255, verbose_name='Вопрос')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('start_date', models.DateField(verbose_name='Начало')),
                ('end_date', models.DateField(verbose_name='Окончание')),
                ('vote_type', models.CharField(choices=[('share', 'Долями'), ('account', 'Голосами')], default='account', max_length=255, verbose_name='Тип голосования')),
                ('status', models.CharField(choices=[('active', 'Активно'), ('finished', 'Завершен')], default='active', max_length=255, verbose_name='Статус')),
                ('quorum', models.IntegerField(choices=[(50, '>50%'), (60, '>60%'), (70, '>70%'), (80, '>80%'), (90, '>90%'), (100, '100%')], default=50, verbose_name='Кворум')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_created_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Голосования',
                'verbose_name_plural': 'Голосования',
            },
        ),
        migrations.CreateModel(
            name='VoteMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.IntegerField(choices=[(1, 'ЗА'), (2, 'ПРОТИВ'), (3, 'ВСЕ РАВНО')], default=1)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_votes', to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vote_members', to='vote.vote')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
            },
        ),
    ]