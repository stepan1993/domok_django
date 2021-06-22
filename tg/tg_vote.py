import datetime
import logging
from vote.models import Vote, VoteMember
from users.models import Account, CustomUser
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater,CommandHandler,MessageHandler, Filters,ConversationHandler,CallbackContext)
import tg.tg_config   as conf

def get_votes(update):
    account = Account.objects.get(custom_user__telegram_id = update.message.from_user.id)
    votes =  Vote.objects.filter(start_date__lte=datetime.date.today(),object_id=account.object_id).order_by('-created_at')
    result = []
    for index,vote in enumerate(votes):
        status = ""
        if vote.is_active:
            status = "Активно"
        elif vote.is_past_due:
            if account.custom_user.role == "moderator"  or account.custom_user.role == "worker":
                status = "Завершен"
            else:
                if vote.members_count_percentage >= vote.quorum:
                    status = "Завершен"
                else:
                    status = "Не состоялось"
        result.append({
                    "index":index,
                    "status":status,
                    "question":vote.question,
                    "vote":vote
                    })
    return result

def vote(update: Update, _: CallbackContext) -> int:
    text = update.message.text
    vote = get_votes(update)[int(text[0:text.index('.')])-1]
    account = Account.objects.get(custom_user__telegram_id = update.message.from_user.id)
    current_user_vote = 0 if vote['vote'].vote_members.filter(member_id =account.custom_user_id).count() == 0 \
                            else vote['vote'].vote_members.filter(member_id =account.custom_user_id).first().point
    
    print(current_user_vote)
    if vote['vote'].is_active:
        reply_keyboard = [["ЗА"],["ПРОТИВ"],["ВСЕ РАВНО"],['НЕ ГОЛОСОВАТЬ']]
        conf.WRITTEN_DATA['vote'][update.message.from_user.id] = vote['vote'].id
    else:
        reply_keyboard = conf.LOGGED_IN_ITEMS

    update.message.reply_text(
        "Вопрос - "+vote['vote'].question+"\n"\
        +"Описание - "+vote['vote'].description+"\n"\
        +str(vote['vote'].start_date)+" - "+str(vote['vote'].end_date)+"\n"\
        +"Всего проголосовало - "+str(round(vote['vote'].members_count_percentage))+"%\n"\
        +"Ваш Вклад - "+str("ЗА" if current_user_vote == 1 else "ПРОТИВ" if current_user_vote == 2 else "ВСЕ РАВНО" if current_user_vote == 3 else "НЕ УЧАСТВОВАЛИ")+"\n"\
        +"Статус - "+vote['status'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    if vote['vote'].is_active:
        return conf.VOTING_PROCESS
    else:
        return conf.SELECTION

def voting_process(update: Update, _: CallbackContext) -> int:
    if update.message.text == "ЗА":
        vote = 1
    elif update.message.text == "ПРОТИВ":
        vote = 2
    elif update.message.text == "ВСЕ РАВНО":
        vote = 3
    else:
        update.message.reply_text(
            "Выберите что-нибудь.",
            reply_markup=ReplyKeyboardMarkup(conf.LOGGED_IN_ITEMS, one_time_keyboard=True),
        )
        return conf.SELECTION
    try:
        voting = VoteMember.objects.get(vote_id = conf.WRITTEN_DATA['vote'][update.message.from_user.id],
                                member__telegram_id = update.message.from_user.id)
        voting.point = vote
        voting.save()
    except:
        account = Account.objects.get(custom_user__telegrm_id = update.message.from_user.id)
        VoteMember(vote_id = conf.WRITTEN_DATA['vote'][update.message.from_user.id],
                                member_id = account.custom_user_id,
                                point=vote).save()
    update.message.reply_text(
            "Ваше голосование успешно принято.",
            reply_markup=ReplyKeyboardMarkup(conf.LOGGED_IN_ITEMS, one_time_keyboard=True),
        )
    return conf.SELECTION

