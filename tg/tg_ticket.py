import logging
from service.models import Service
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InputMediaDocument
from telegram.ext import (Updater,CommandHandler,MessageHandler, Filters,ConversationHandler,CallbackContext)
import tg.tg_config as conf
from django.contrib.auth.hashers import check_password
from users.models import Account, CustomUser
import datetime
from ticket.models import Comment, CommentFile, Ticket, TicketFile, TicketStatusHistory

def get_tickets(update):
    account = Account.objects.get(custom_user__telegram_id = update.message.from_user.id)
    tickets =  Ticket.objects.filter(object_id=account.object_id).order_by('-id')
    result = []
    for index,ticket in enumerate(tickets):
        status = ""
        if ticket.status == 1:
            status ="На рассмотрении"
        elif ticket.status == 2:
            status = "Принято к исполнению"
        elif ticket.status == 3:
            status = "Выполнено"
        if ticket.finished and ticket.finish_accepted:
            status +="/ Подтверждено"
        elif ticket.finished and not ticket.finish_accepted:
            status += "/ Не подтверждено"
        result.append({
                    "index":index,
                    "status":status,
                    "problem":ticket.problem,
                    "ticket":ticket
                    })
    return result

def get_services():
    return [[service.dative] for service in  Service.objects.all()]

def ticket(update: Update, _: CallbackContext) -> int:
    text = update.message.text
    ticket = get_tickets(update)[int(text[0:text.index('.')])-1]
    reply_buttons = [['Все сообщения'],['Добавить комментарий'],['Главное меню']]
    if ticket['ticket'].finished and not ticket['ticket'].finish_accepted:
        reply_buttons.insert(0,["Отклонить решение"])
        reply_buttons.insert(0,["Подтвердить решение"])
        
    files = ""
    conf.WRITTEN_DATA['selected_ticket'][update.message.from_user.id]=ticket
    for file in ticket['ticket'].ticket_files.all():
        files+=str(file.file)+" ("+file.size+" Кб)\n"
    update.message.reply_text(
        "Проблема - "+ticket['ticket'].problem+"\n"\
        +"Кому - " + ticket['ticket'].whom.dative+"\n"\
        +"Дата - " + str(ticket['ticket'].created_date.strftime("%d.%m.%Y (%H:%M)"))+"\n"\
        +"Описание - "+ticket['ticket'].description+"\n"\
        +"Статус - "+ticket['status']+"\n"\
        +files,
        reply_markup=ReplyKeyboardMarkup(reply_buttons, one_time_keyboard=True),
    )
    return conf.TICKET_DETAILS

def whom(update: Update, _: CallbackContext) -> int:
    conf.WRITTEN_DATA['ticket'].append({
        update.message.from_user.id:{"whom":update.message.text},
    })
    update.message.reply_text(
        'Назавите проблему',
        reply_markup=ReplyKeyboardRemove(),
    )
    return conf.TICKET_TITLE

def title(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['ticket']))[0]
    existing[update.message.from_user.id]['title'] = update.message.text
    existing[update.message.from_user.id]['file'] = []
    update.message.reply_text(
        'Подробнее о проблеме',
        reply_markup=ReplyKeyboardRemove(),
    )
    return conf.TICKET_DESCRIBTION

def description(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['ticket']))[0]
    existing[update.message.from_user.id]['description'] = update.message.text
    update.message.reply_text(
        'Выберите',
        reply_markup=ReplyKeyboardMarkup([['Добавить файл'],['Добавить фото'],['Сохранить']], one_time_keyboard=True),
    )
    return conf.TICKET_SELECTION

def file(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['ticket']))[0][update.message.from_user.id]
    existing['file'].append(update.message)
    update.message.reply_text(
        'Выберите',
        reply_markup=ReplyKeyboardMarkup([['Добавить файл'],['Добавить фото'],['Сохранить']], one_time_keyboard=True),
    )
    return conf.TICKET_SELECTION

def photo(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['ticket']))[0][update.message.from_user.id]
    existing['file'].append(update.message)
    update.message.reply_text(
        'Выберите',
        reply_markup=ReplyKeyboardMarkup([['Добавить файл'],['Добавить фото'],['Сохранить']], one_time_keyboard=True),
    )
    return conf.TICKET_SELECTION

def ticket_selection(update: Update, _: CallbackContext) -> int:
    if update.message.text == "Все сообщения":
        tickets = get_tickets(update)
        if len(tickets) > 0 :            
            keyboard = [[str(ticket['index']+1)+"."+ticket['problem']+" - "+ticket['status']] for ticket in tickets]
            update.message.reply_text(
                'Выберите сообщения о проблеме',
                reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
            )
            return conf.TICKET
    if update.message.text == "Главное меню":
        update.message.reply_text(
                'Выберите сообщения о проблеме',
                reply_markup=ReplyKeyboardMarkup(conf.LOGGED_IN_ITEMS, one_time_keyboard=True),
            )
        return conf.SELECTION
    if update.message.text == "Добавить файл":
        update.message.reply_text(
            'Прикрепите один файл',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.TICKET_FILE
    if update.message.text == "Добавить фото":
        update.message.reply_text(
            'Прикрепите один фото',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.TICKET_PHOTO
    else:
        existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['ticket']))[0][update.message.from_user.id]
        account = Account.objects.get(custom_user__telegram_id = update.message.from_user.id)
        ticket = Ticket(object_id = account.object_id,
                        whom_id = Service.objects.get(dative=str(existing['whom']).strip()).id,
                        author_id = account.custom_user_id,
                        problem = str(existing['title']).strip(),
                        description = str(existing['description']).strip())
        ticket.save()
        TicketStatusHistory(user_id = account.custom_user_id, ticket=ticket, status=1).save()
        try:
            if existing['file']:
                for item in existing['file']:
                    if item['document']:
                        photo_file = item['document']
                        file_name = photo_file['file_unique_id']+"."+photo_file["file_name"].split(".")[-1]
                        photo_file.get_file().download("media/ticket/"+file_name)
                        TicketFile(ticket_id = ticket.id, file=file_name,size =round(int(photo_file['file_size'])/1024,2)).save()
                    elif item['photo']:
                        photo_file = item.photo[-1].get_file()
                        file_name = photo_file['file_unique_id']+"."+photo_file["file_path"].split(".")[-1]
                        photo_file.download("media/ticket/"+file_name)
                        TicketFile(ticket_id = ticket.id, file=file_name,size =round(int(photo_file['file_size'])/1024,2)).save()
        except:
            pass
        update.message.reply_text(
            '\"'+ticket.problem+'" прблем успешно сохронен.',
            reply_markup=ReplyKeyboardMarkup(conf.LOGGED_IN_ITEMS, one_time_keyboard=True),
        )
        return conf.SELECTION

def ticket_details_selection(update: Update, _: CallbackContext) -> int:
    if update.message.text == "Комментарий":
        tick = conf.WRITTEN_DATA['selected_ticket'][update.message.from_user.id]['ticket']
        text = ""
        comments = Comment.objects.filter(ticket_id=tick.id)
        if comments.count()>0:
            for comment in comments:
                text+=comment.author.first_name+" "+comment.author.last_name+"\n"\
                    +comment.comment+"\n"
                for file in comment.comment_files.all():
                    text+=str(file.file)
                text+="\n"+str(comment.date.strftime("%d.%m.%Y (%H:%M)"))+"\n_______________________________\n"
        else:
            text = "Нет Комментарий"
        reply_buttons = [['Все сообщения'],['Добавить комментарий'],['Главное меню']]
        if tick.finished and not tick.finish_accepted:
            reply_buttons.insert(0,["Отклонить решение"])
            reply_buttons.insert(0,["Подтвердить решение"])
            
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(reply_buttons, one_time_keyboard=True),
        )
        return conf.TICKET_DETAILS

    elif update.message.text == "Добавить комментарий":
        update.message.reply_text(
            'Напишите комментарий',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.TICKET_NEW_COMMENT_SELECTION1
    elif update.message.text == "Подтвердить решение" or update.message.text == "Отклонить решение" or update.message.text == "Все сообщения":
        account = Account.objects.get(custom_user__telegram_id = update.message.from_user.id)
        if update.message.text == "Подтвердить решение":
            ticket = conf.WRITTEN_DATA['selected_ticket'][update.message.from_user.id]['ticket']
            ticket.finish_accepted = True
            ticket.save()
            TicketStatusHistory(user=account.custom_user, ticket=ticket, status=3).save()
        elif update.message.text == "Отклонить решение":
            ticket = conf.WRITTEN_DATA['selected_ticket'][update.message.from_user.id]['ticket']
            ticket.status = 2
            ticket.finished = False
            ticket.finish_accepted = False
            ticket.save()
            TicketStatusHistory(user=account.custom_user, ticket=ticket, status=2).save()
        tickets = get_tickets(update)
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
    else:
        update.message.reply_text(
                'Выберите что-нибудь.',
                reply_markup=ReplyKeyboardMarkup(conf.LOGGED_IN_ITEMS, one_time_keyboard=True),
            )
        return conf.SELECTION

def ticket_comment_selection(update: Update, _: CallbackContext) -> int:
    try:
        existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['new_ticket']))[0][update.message.from_user.id]=[]
    except:
        pass
    conf.WRITTEN_DATA['new_ticket'].append({
        update.message.from_user.id:{"comment":update.message.text,
                                    "file":[],
                                    'ticket_id':conf.WRITTEN_DATA['selected_ticket'][update.message.from_user.id]['ticket'].id},
    })
    update.message.reply_text(
        'Выберите',
        reply_markup=ReplyKeyboardMarkup([['Добавить фото'],['Добавить файл'],['Сохранить']], one_time_keyboard=True),
    )
    return conf.TICKET_NEW_COMMENT_SELECTION2

def ticket_comm(update: Update, _: CallbackContext) -> int:
    if update.message.text == "Добавить файл":
        existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['ticket']))[0][update.message.from_user.id]
        existing['file'].append(update.message)
        update.message.reply_text(
            'Прикрепите один файл',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.TICKET_NEW_COMMENT_FILE
    if update.message.text == "Добавить фото":
        existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['new_ticket']))[0][update.message.from_user.id]
        existing['file'].append(update.message)
        update.message.reply_text(
            'Прикрепите один фото',
            reply_markup=ReplyKeyboardRemove(),
        )
        return conf.TICKET_NEW_COMMENT_PHOTO
    if update.message.text == "Сохранить":
        existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['new_ticket']))[0][update.message.from_user.id]
        account = Account.objects.get(custom_user__telegram_id = update.message.from_user.id)
        comment = Comment(ticket_id = existing['ticket_id'],
                        comment = existing['comment'],
                        author_id = account.custom_user_id)
        comment.save()
        try:
            if existing['file']:
                for item in existing['file']:
                    if item['document']:
                        photo_file = item['document']
                        file_name = photo_file['file_unique_id']+"."+photo_file["file_name"].split(".")[-1]
                        photo_file.get_file().download("media/ticket/"+file_name)
                        CommentFile(comment_id = comment.id, file=file_name,size =round(int(photo_file['file_size'])/1024,2)).save()
                    elif item['photo']:
                        photo_file = item.photo[-1].get_file()
                        file_name = photo_file['file_unique_id']+"."+photo_file["file_path"].split(".")[-1]
                        photo_file.download("media/ticket/"+file_name)
                        CommentFile(comment_id = comment.id, file=file_name,size =round(int(photo_file['file_size'])/1024,2)).save()
        except:
            pass
        update.message.reply_text(
            '\"'+comment.comment+'" комментарий успешно сохронен.',
            reply_markup=ReplyKeyboardMarkup(conf.LOGGED_IN_ITEMS, one_time_keyboard=True),
        )
        return conf.SELECTION

def new_comment_file(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['new_ticket']))[0][update.message.from_user.id]
    existing['file'].append(update.message)
    update.message.reply_text(
        'Выберите',
        reply_markup=ReplyKeyboardMarkup([['Добавить файл'],['Добавить фото'],['Сохранить']], one_time_keyboard=True),
    )
    return conf.TICKET_NEW_COMMENT_SELECTION2

def new_comment_photo(update: Update, _: CallbackContext) -> int:
    existing = list(filter(lambda x: x.get(update.message.from_user.id), conf.WRITTEN_DATA['new_ticket']))[0][update.message.from_user.id]
    existing['file'].append(update.message)
    update.message.reply_text(
        'Выберите',
        reply_markup=ReplyKeyboardMarkup([['Добавить файл'],['Добавить фото'],['Сохранить']], one_time_keyboard=True),
    )
    return conf.TICKET_NEW_COMMENT_SELECTION2

