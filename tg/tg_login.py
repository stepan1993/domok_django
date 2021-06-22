import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater,CommandHandler,MessageHandler, Filters,ConversationHandler,CallbackContext)
import tg.tg_config as conf
from django.contrib.auth.hashers import check_password
from users.models import CustomUser

def check_if_logged_in(update):
    return CustomUser.objects.filter(telegram_id=update.message.from_user.id).count()>0

def logout(update):
    users = CustomUser.objects.filter(telegram_id=update.message.from_user.id)
    for user in users:
        user.telegram_id = None
        user.save()
    return True

def login_password(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['login']))
    if len(existing) == 0:
        conf.WRITTEN_DATA['login'].append({
            update.message.from_user.id:update.message.text,
        })
    else:
        existing[0][update.message.from_user.id]=update.message.text
    update.message.reply_text(
        'Пароль пользователя',
        reply_markup=ReplyKeyboardRemove(),
    )
    return conf.LOGIN

def login(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['login']))[0]
    username = existing[update.message.from_user.id]
    password = update.message.text
    try:
        user = CustomUser.objects.get(username=username)
        
        if check_password(password, user.password):
            if user.role == "client":
                user.telegram_id = update.message.from_user.id
                user.save()
                reply_keyboard = conf.LOGGED_IN_ITEMS
                update.message.reply_text(
                    str(user.first_name+" " + user.last_name) +' Вы успешно вошли в систему ',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                )
                return conf.SELECTION
            else:
                reply_keyboard = conf.UNLOGGED_IN_ITEMS
                update.message.reply_text(
                    str(user.first_name+" " + user.last_name) +' Только клиенты могут авторизоваться через телеграмму.',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                )
                return conf.SELECTION
        else:
            reply_keyboard = conf.UNLOGGED_IN_ITEMS

            update.message.reply_text(
                'Неверное имя пользователя или пароль',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
            )
            return conf.SELECTION
    except:
        reply_keyboard = conf.UNLOGGED_IN_ITEMS
        update.message.reply_text(
            'Неверное имя пользователя или пароль',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
        return conf.SELECTION
