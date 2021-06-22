#https://developers.viber.com/docs/api/python-bot-api/
# https://partners.viber.com/account/5582320141219647583/info
# https://github.com/Viber/viber-bot-python


from viberbot.api.messages import RichMediaMessage, KeyboardMessage
from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
import logging
import sched
import threading
import time
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


app = Flask(__name__)
viber = Api(BotConfiguration(
    name='DOMMMM OKKKKKKKK',
    avatar='http://site.com/avatar.jpg',
    auth_token='4d7862978fe7d05f-4858d39006324b79-d0a6b7ecf1905ad1',
))


@app.route('/incomings', methods=['POST'])
def incoming():

	SAMPLE_KEYBOARD = {
	"Type": "keyboard",
	"Buttons": [
		{
		"Columns": 6,
		"Rows": 1,
		"BgColor": "#e6f5ff",
		"BgMedia": "http://link.to.button.image",
		"BgMediaType": "picture",
		"BgLoop": True,
		"ActionType": "reply",
		"ActionBody": "This will be sent to your bot in a callback",
		"ReplyType": "message",
		"Text": "Push me!"
		},{
		"Columns": 6,
		"Rows": 1,
		"BgColor": "#e6f5ff",
		"BgMedia": "http://link.to.button.image",
		"BgMediaType": "picture",
		"BgLoop": True,
		"ActionType": "reply",
		"ActionBody": "This will be sent to your bot in a callback 2",
		"ReplyType": "message",
		"Text": "Push me 2!"
		}
		]
	}

	message = KeyboardMessage(tracking_data='tracking_data', keyboard=SAMPLE_KEYBOARD)
	logger.debug("received request. post data: {0}".format(request.get_data()))

	viber_request = viber.parse_request(request.get_data().decode('utf8'))
	if isinstance(viber_request, ViberMessageRequest):
		viber.send_messages(viber_request.sender.id, [
			message
		])
	elif isinstance(viber_request, ViberConversationStartedRequest) \
			or isinstance(viber_request, ViberSubscribedRequest) \
			or isinstance(viber_request, ViberUnsubscribedRequest):
		viber.send_messages(viber_request.sender.id, [
			TextMessage(None, None, viber_request.get_event_type())
		])
	elif isinstance(viber_request, ViberFailedRequest):
		logger.warn("client failed receiving message. failure: {0}".format(viber_request))
	return Response(status=200)

def set_webhook(viber):
	viber.set_webhook('https://dom.annaniks.com:4444/incomings')

if __name__ == "__main__":
	scheduler = sched.scheduler(time.time, time.sleep)
	scheduler.enter(5, 1, set_webhook, (viber,))
	t = threading.Thread(target=scheduler.run)
	t.start()

	context = ('fullchain.pem', 'privkey.pem')
	app.run(host='0.0.0.0', port=4444, debug=True, ssl_context=context)

