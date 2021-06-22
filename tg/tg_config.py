SELECTION = 0
REGISTER, LOGIN, VOTE = range(1,4)
FIRSTNAME, LASTNAME, MIDDLENAME, PHONENUMBER, EMAIL, ACCOUNT, PASSWORD, REPEATPASSWORD = range(4,12)
LOGIN_PASSWORD = 12
LOGOUT = 13
VOTING_PROCESS = 14
TICKET, WHOM, TICKET_TITLE, TICKET_DESCRIBTION, TICKET_SELECTION, TICKET_SAVE, TICKET_FILE, TICKET_PHOTO = range(15,23)
TICKET_DETAILS, TICKET_COMMENTS, TICKET_NEW_COMMENT,TICKET_NEW_COMMENT_FILE,TICKET_NEW_COMMENT_PHOTO, TICKET_NEW_COMMENT_SELECTION1,TICKET_NEW_COMMENT_SELECTION2 = range(23,30)  
TICKET_ITEMS = [['Комментарий'],['Добавить комментарий'],['Главное меню']]
UNLOGGED_IN_ITEMS = [['Вход в личный кабинет'],['Регистрация']]
LOGGED_IN_ITEMS = [['Голосования'],['Все сообщения'],['Сообщить о проблеме'],['Выход']]
WRITTEN_DATA = {
    "login":[],
    "register":[],
    "vote":{},
    "ticket":[],
    "selected_ticket":{},
    "new_ticket":[]
}