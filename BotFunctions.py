# -*- coding: utf-8 -*-
import re
import logging
from MorseCode import *
current = []

def send_welcome():
	return "Bienvenido al traductor de codigo morse."
def send_goodbye():
	return "No te odio. Adios. x_x"

def send_about():
	return "Author: Rey David Dominguez\nTelegram: @Tecnologer\nEmail: rdominguez@tecnologer.net\nCodigo fuente: "

def send_decrypt(message):
	global current
	decryptedMessage = ""
	morseCode = re.sub("/decrypt\s?(@MorsingBot)?","",message["text"], flags=re.IGNORECASE)
	user = "Humano"
	if message["from"]["first_name"] != "" and message["from"]["first_name"] != None:
		user = message["from"]["first_name"]
	elif message["from"]["username"] != "" and message["from"]["username"] != None:
		user = message["from"]["username"]

	# morseCode = message["text"].replace("/decrypt ","")
	if morseCode.strip() == "":
		addNewCurrentCommand(message, "decrypt")
		decryptedMessage = user+" por favor escribe el codigo morse (solo puntos y guiones) a desencriptar:"
	else:
		decryptedMessage = decrypt(morseCode)
		if decryptedMessage == "":
			decryptedMessage = "Lo siento "+user+" no pude desencriptar tu mensaje "+u'\U0001f61e'+u'\U0001f61e'

	return decryptedMessage

def send_encrypt(message):
	global current
	encryptedMessage = ""
	text = re.sub("/encrypt\s?(@MorsingBot)?","",message["text"], flags=re.IGNORECASE)
	user = "Humano"
	if message["from"]["first_name"] != "" and message["from"]["first_name"] != None:
		user = message["from"]["first_name"]
	elif message["from"]["username"] != "" and message["from"]["username"] != None:
		user = message["from"]["username"]

	if text == "":
		addNewCurrentCommand(message, "encrypt")		
		encryptedMessage = user+" por favor escribe el mensaje (con alfabeto latino) a encriptar:"
	else:
		encryptedMessage = encrypt(text)
		if encryptedMessage == "":
			encryptedMessage = "Lo siento "+user+" no pude encriptar tu mensaje "+u'\U0001f61e'+u'\U0001f61e'

	return encryptedMessage		

def echo_all(message):
	global current
	print(current)
	index = getPositionCurrentCommand(message)
	msg = ""
	if index>-1:
		if current[index]["type"] == "decrypt":
			msg = send_decrypt(message)
		elif current[index]["type"] == "encrypt":
			msg = send_encrypt(message)

		del current[index]

	return msg
	# else:
	# 	bot.reply_to(message, "Codigo incorrecto")

def decrypt(morseCode):
	message = ""
	MorseMessage = re.split(' |\n|\|',morseCode) #morseCode.split(" ")
	for x in MorseMessage:
		inputVal = list(x)
		morseAux = getMorseCode()

		for i in inputVal:
			if i == "." and morseAux is not None:
				morseAux = morseAux["left"]
			elif i == "-" and morseAux is not None:
				morseAux = morseAux["rigth"]
			elif i == "—".decode('utf-8') and morseAux is not None:
				morseAux = morseAux["rigth"]
				morseAux = morseAux["rigth"]

		if morseAux is not None:
			message += morseAux["data"]

	return message

def encrypt(message):
	messageEncrypted = "";
	alphabet = getAlphabetCode()
	message = message.upper()
	inputMessage = list(message)
	for key in inputMessage:
		if key in alphabet:
			messageEncrypted = messageEncrypted + alphabet[key]+" ";

	return messageEncrypted;

def addNewCurrentCommand(message, _type):
	global current
	index = getPositionCurrentCommand(message)
	if index > -1 or len(current) == 0:
		newCurrent = {"type": _type, "user_id": message["from"]["id"], "group_id": message["chat"]["id"]}
		current.append(newCurrent)

def getPositionCurrentCommand(message):
	global current

	i = 0
	for command in current:
		if command["user_id"] == message["from"]["id"] and command["group_id"] == message["chat"]["id"]:
			return i
		i+=1

	return -1