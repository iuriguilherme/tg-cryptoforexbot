# vim:fileencoding=utf-8

import datetime
import re
import time
import ConfigParser

try:
	import telepot
except tuple(ImportError, NameError):
	print "You have to `pip install telepot`. Try again when you do."
	exit()

from cryptoforexbot import texts

class cryptoforex():

	def __init__(self):
		self.log_INFO(str("Starting %s" % (__name__)))
		self.config = ConfigParser.ConfigParser()
		try:
			self.config.read("cryptoforexbot/cryptoforexbot.cfg")
			## If you replace the following line with something like
			##   self.token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
			##   , it will work too. Your code will be ugly, however.
			self.token = self.config.get("botfather", "token")
		except ConfigParser.NoSectionError:
			self.log_ERR(str(texts.err_config))
			self.log_INFO(str("Exiting %s." % (__name__)))
			return
		try:
			self.bot = telepot.Bot(self.token)
			self.bot.message_loop(self.rcv)
		except Exception as e:
			self.log_ERR(str("Telegram error: %s" % (e)))
			pass
		while 1:
			try:
				time.sleep(10)
			except KeyboardInterrupt:
				self.log_INFO(str("Exiting %s." % (__name__)))
				return

	## Standard output debugging
	def log_INFO(self, message):
		now = str(datetime.datetime.now())
		print '[%s] INFO: %s' % (now, message)
	def log_ERR(self, message):
		now = str(datetime.datetime.now())
		print '[%s] ERR: %s' % (now, message)
	def log_CMD(self, command):
		now = str(datetime.datetime.now())
		print '[%s] CMD: Running %s' % (now, command)
	def log_RCV(self, message, target):
		now = str(datetime.datetime.now())
		print '[%s] RCV: Received "%s" from %s' % (now, message, target)
	def log_SEND(self, message, target):
		now = str(datetime.datetime.now())
		print '[%s] SEND: Sending "%s" to %s' % (now, message, target)

	def group_commands(self, command, chat_id):
		reply = str()
		if command == '/help@cryptoforexbot':
			self.log_CMD(str(command))
			reply = str(texts.help)
			self.log_SEND(str(reply), str(chat_id))
			self.bot.sendMessage(chat_id, reply)
		elif command == '/info@cryptoforexbot':
			self.log_CMD(str(command))
			reply = str(texts.info)
			self.log_SEND(str(reply), str(chat_id))
			self.bot.sendMessage(chat_id, reply)
	def user_commands(self, command, chat_id):
		reply = str("I'm not sure what a '%s' is. Perhaps you should try /help" % (command))
		if re.search('^/help', command):
			self.log_CMD(str(command))
			reply = str(texts.help)
		elif re.search('^/info', command):
			self.log_CMD(str(command))
			reply = str(texts.info)
		self.log_SEND(str(reply), str(chat_id))
		self.bot.sendMessage(chat_id, reply)

	def rcv(self, msg):
		chat_id = int(msg['chat']['id'])
		command = str(re.compile('/\W+').sub(' ', msg['text']).strip())
		self.log_RCV(str(command),str(chat_id))
		## If chat_id is negative, then we're talking with a group.
		##	therefore, we'll answer only if we're being directly addressed
		##	(command must include bot name).
		##	Otherwise, we answer any command
		if chat_id < 0:
			self.group_commands(str(command), str(chat_id))
		else:
			self.user_commands(str(command), str(chat_id))

