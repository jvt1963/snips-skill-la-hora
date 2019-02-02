#!/usr/bin/env python3
from hermes_python.hermes import Hermes
from datetime import datetime
from pytz import timezone

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def verbalise_hour(i):
	now = datetime.now(timezone('Europe/Madrid'))
	if now.minute > 30:
		i = i + 1
	if i > 12:
		i = i - 12
	if i == 0:
		return "doce"
	elif i == 1:
		return "una"
	else:
		return "{0}".format(str(i)) 

def verbalise_minute(i):
	if i > 30:
		i = 60 - i
	if i == 0:
		return ""
	elif i == 15:
		return "cuarto"
	elif i == 30:
		return "media"
	else:
		return "{0}".format(str(i)) 


def intent_received(hermes, intent_message):

	print()
	print((intent_message.intent.intent_name))
	print()

	if intent_message.intent.intent_name == 'gplaza:askTime':


		print((intent_message.intent.intent_name))
		now = datetime.now(timezone('Europe/Madrid'))
				
		if verbalise_hour(now.hour) == "una":
			sentence = 'Es la '
		else:
			sentence = 'Son las '
		
		sentence += verbalise_hour(now.hour) + " " 

		if now.minute == 0:
			sentence += 'en punto'
		elif now.minute < 31:
			sentence += 'y ' + verbalise_minute(now.minute)
		else:
			sentence += 'menos ' + verbalise_minute(now.minute)

		if now.hour > 12:
			sentence += " de la tarde"

		print(sentence)

		hermes.publish_end_session(intent_message.session_id, sentence)

	elif intent_message.intent.intent_name == 'gplaza:greetings':

		hermes.publish_end_session(intent_message.session_id, "De nada!")


with Hermes(MQTT_ADDR) as h:
	h.subscribe_intents(intent_received).start()
