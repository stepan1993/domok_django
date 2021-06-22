#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
#https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'domok'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "domok.settings")
import django
django.setup()
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater,
CommandHandler,MessageHandler, Filters,

ConversationHandler,CallbackContext)
import tg.tg_config  as conf
import tg.tg_login as login
import tg.tg_register as register
import tg.tg_vote as vote
import tg.tg_ticket as ticket

def selection(update: Update, _: CallbackContext) -> int:
    if update.message.text == "Вход в личный кабинет":
        update.message.reply_text(
            'Имя пользователя',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.LOGIN_PASSWORD
    elif update.message.text == "Регистрация":
        update.message.reply_text(
            'Введите лицевой счет',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.REGISTER
    elif update.message.text == "Выход":
        reply_keyboard = conf.UNLOGGED_IN_ITEMS
        login.logout(update)
        update.message.reply_text(
            'Вы успешно вышли из системы',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
        return conf.SELECTION
    elif update.message.text == "Голосования":
        votes = vote.get_votes(update)
        if len(votes) > 0 :            
            keyboard = [[str(vote['index']+1)+"."+vote['question']+" - "+vote['status']] for vote in votes]
            update.message.reply_text(
                'Выберите Вопрос на голосование',
                reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
            )
            return conf.VOTE
        else:
            update.message.reply_text(
                'Нет активных голосований',
                reply_markup=ReplyKeyboardMarkup(conf.LOGGED_IN_ITEMS, one_time_keyboard=True),
            )
            return conf.SELECTION
    elif update.message.text == "Все сообщения":
        tickets = ticket.get_tickets(update)
        if len(tickets) > 0 :            
            keyboard = [[str(ticket['index']+1)+"."+ticket['problem']+" - "+ticket['status']] for ticket in tickets]
            update.message.reply_text(
                'Выберите сообщения о проблеме',
                reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
            )
            return conf.TICKET
        else:
            update.message.reply_text(
                'Нет проблемы',
                reply_markup=ReplyKeyboardMarkup(conf.LOGGED_IN_ITEMS, one_time_keyboard=True),
            )
            return conf.SELECTION
    elif update.message.text == "Сообщить о проблеме":
        update.message.reply_text(
            'Кому',
            reply_markup=ReplyKeyboardMarkup(ticket.get_services(), one_time_keyboard=True),
        )
        return conf.WHOM
    else:
        update.message.reply_text(
            'You choose nothing',
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

def start(update: Update, _: CallbackContext) -> int:
    if login.check_if_logged_in(update):
        reply_keyboard = conf.LOGGED_IN_ITEMS
    else:
        reply_keyboard = conf.UNLOGGED_IN_ITEMS
    update.message.reply_text(
        'Выберите что-нибудь.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return conf.SELECTION

def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def tg() -> None:
    #prod
    # updater = Updater('1811883236:AAEFky1NdpBd0AnJjNR97NQg5mMJXVU-Hys')
    # #dev
    updater = Updater('1860582544:AAHfG2wUhBUeoMmXdh27VTQOue5i_T8KK7I')
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            conf.SELECTION: [MessageHandler(Filters.text, selection)],
            conf.REGISTER: [MessageHandler(Filters.text, register.register), CommandHandler('cancel', cancel)],
            conf.LOGIN: [MessageHandler(Filters.text, login.login), CommandHandler('cancel', cancel)],

            conf.VOTE: [MessageHandler(Filters.text, vote.vote), CommandHandler('cancel', cancel)],
            conf.VOTING_PROCESS: [MessageHandler(Filters.text, vote.voting_process), CommandHandler('cancel', cancel)],

            conf.LOGIN_PASSWORD: [MessageHandler(Filters.text, login.login_password), CommandHandler('cancel', cancel)],

            conf.TICKET: [MessageHandler(Filters.text, ticket.ticket), CommandHandler('cancel', cancel)],
            conf.TICKET_TITLE: [MessageHandler(Filters.text, ticket.title), CommandHandler('cancel', cancel)],
            conf.TICKET_DESCRIBTION: [MessageHandler(Filters.text, ticket.description), CommandHandler('cancel', cancel)],
            conf.WHOM: [MessageHandler(Filters.text, ticket.whom), CommandHandler('cancel', cancel)],
            conf.TICKET_FILE: [MessageHandler(Filters.all, ticket.file), CommandHandler('cancel', cancel)],
            conf.TICKET_SELECTION: [MessageHandler(Filters.text, ticket.ticket_selection), CommandHandler('cancel', cancel)],
            conf.TICKET_PHOTO: [MessageHandler(Filters.photo, ticket.photo), CommandHandler('cancel', cancel)],
            conf.TICKET_DETAILS: [MessageHandler(Filters.text, ticket.ticket_details_selection), CommandHandler('cancel', cancel)],
            conf.TICKET_NEW_COMMENT_PHOTO: [MessageHandler(Filters.photo, ticket.new_comment_photo), CommandHandler('cancel', cancel)],
            conf.TICKET_NEW_COMMENT_FILE: [MessageHandler(Filters.all, ticket.new_comment_file), CommandHandler('cancel', cancel)],
            conf.TICKET_NEW_COMMENT_SELECTION1: [MessageHandler(Filters.text, ticket.ticket_comment_selection), CommandHandler('cancel', cancel)],
            conf.TICKET_NEW_COMMENT_SELECTION2: [MessageHandler(Filters.text, ticket.ticket_comm), CommandHandler('cancel', cancel)],


            conf.REGISTER: [MessageHandler(Filters.text, register.register), CommandHandler('cancel', cancel)],
            conf.FIRSTNAME: [MessageHandler(Filters.text, register.first_name), CommandHandler('cancel', cancel)],
            conf.LASTNAME: [MessageHandler(Filters.text, register.last_name), CommandHandler('cancel', cancel)],
            conf.MIDDLENAME: [MessageHandler(Filters.text, register.middle_name), CommandHandler('cancel', cancel)],
            conf.PHONENUMBER: [MessageHandler(Filters.text, register.phone_number), CommandHandler('cancel', cancel)],
            conf.EMAIL: [MessageHandler(Filters.text, register.email), CommandHandler('cancel', cancel)],
            conf.PASSWORD: [MessageHandler(Filters.text, register.password), CommandHandler('cancel', cancel)],
            conf.REPEATPASSWORD: [MessageHandler(Filters.text, register.repeat_password), CommandHandler('cancel', cancel)],
        },
        allow_reentry = True,
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
    while True:
        sleep(5)

tg()
from time import sleep
from daemonize import Daemonize

pid = "/tmp/tg.pid"

daemon = Daemonize(app="domok", pid=pid, action=tg)
daemon.start()