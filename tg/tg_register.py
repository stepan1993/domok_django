import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater,CommandHandler,MessageHandler, Filters,ConversationHandler,CallbackContext)
import tg.tg_config   as conf
from users.models import Account, CustomUser

def register(update: Update, _: CallbackContext) -> int:
    if Account.objects.filter(account=update.message.text).count() == 0:
        update.message.reply_text(
        "Лицевой счет не найден. Попробуйте еще раз.",
        reply_markup=ReplyKeyboardRemove(),
        )
        return conf.REGISTER
    elif CustomUser.objects.filter(username = update.message.text):
        reply_keyboard = conf.UNLOGGED_IN_ITEMS
        update.message.reply_text(
        "По данному лицевому счету уже зарегистрирован пользователь",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
        return conf.SELECTION
    else:
        conf.WRITTEN_DATA['register'].append({
            update.message.from_user.id:{"account":update.message.text},
        })
        update.message.reply_text(
            'Введите Имя',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.FIRSTNAME

def first_name(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['register']))[0]
    existing[update.message.from_user.id]['first_name'] = update.message.text
    update.message.reply_text(
        'Введите Фамилия',
        reply_markup=ReplyKeyboardRemove(),
    )
    return conf.LASTNAME

def last_name(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['register']))[0]
    existing[update.message.from_user.id]['last_name'] = update.message.text
    update.message.reply_text(
        'Введите Отчество',
        reply_markup=ReplyKeyboardRemove(),
    )
    return conf.MIDDLENAME

def middle_name(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['register']))[0]
    existing[update.message.from_user.id]['middle_name'] = update.message.text
    update.message.reply_text(
        'Введите Номер телефона',
        reply_markup=ReplyKeyboardRemove(),
    )
    return conf.PHONENUMBER

def phone_number(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['register']))[0]
    existing[update.message.from_user.id]['phone_number'] = update.message.text
    update.message.reply_text(
        'Введите E-mail',
        reply_markup=ReplyKeyboardRemove(),
    )
    return conf.EMAIL

def email(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['register']))[0]
    existing[update.message.from_user.id]['email'] = update.message.text
    update.message.reply_text(
        'Введите Пароль',
        reply_markup=ReplyKeyboardRemove(),
    )
    return conf.PASSWORD

def password(update: Update, _: CallbackContext) -> int:
    if len(str(update.message.text).strip())<6:
        update.message.reply_text(
            'Пароль дольжен содержить минимум 6 символов. Повторите.',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.PASSWORD
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['register']))[0]
    existing[update.message.from_user.id]['password'] = update.message.text
    update.message.reply_text(
        'Введите пароль еще раз',
        reply_markup=ReplyKeyboardRemove(),
    )
    return conf.REPEATPASSWORD

def repeat_password(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['register']))[0][update.message.from_user.id]
    password = str(existing['password']).strip()
    if str(update.message.text).strip()!=password:
        update.message.reply_text(
            'Пороли не совподают.\n Введите повторний пароль.',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.PASSWORD
    new_user = CustomUser(first_name = str(existing['first_name']).strip(),
                        last_name = str(existing['last_name']).strip(),
                        middle_name = str(existing['middle_name']).strip(),
                        email = str(existing['email']).strip(),
                        username = str(existing['account']).strip(),
                        phone_number = str(existing['phone_number']).strip(),
                        role = "client",
                        telegram_id = update.message.from_user.id,
                        is_active = True)
    new_user.set_password(str(existing['password']).strip())
    new_user.save()
    account = Account.objects.get(account=str(new_user.username).strip())
    account.custom_user_id = new_user.id
    account.save()
    update.message.reply_text(
        str(existing['first_name']) + " " + str(existing['last_name']) + ' Добро пожаловать в DomOK Telegram Bot.',
        reply_markup=ReplyKeyboardMarkup(conf.LOGGED_IN_ITEMS, one_time_keyboard=True),
    )
    return conf.SELECTION
