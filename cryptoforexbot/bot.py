# vim:fileencoding=utf-8
## Telegram bots documentation at https://core.telegram.org/bots
## Telepot documentation at https://telepot.readthedocs.io/en/latest/

import datetime
import re
import time
import ConfigParser

try:
	import telepot
except (ImportError, NameError):
	print "You have to `pip install telepot`. Try again when you do."
	exit()

from cryptoforexbot import metadata, texts

class cryptoforex():

	def __init__(self):
		self.log_INFO(str("Starting %s" % (__name__)))

		self.config_file = str("cryptoforexbot/cryptoforexbot.cfg")
		self.log_INFO(str("Opening config file: %s" % (self.config_file)))
		self.config = ConfigParser.ConfigParser()
		try:
			self.config.read(self.config_file)
			## If you replace the following line with something like
			##   self.token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
			##   , it will work too. Your code will be ugly, however.
			self.token = str(self.config.get("botfather", "token"))
			self.admin_id = int(self.config.get("admin", "id"))
		except ConfigParser.NoSectionError:
			self.log_ERR(str(texts.err_config))
			self.log_INFO(str("Exiting %s." % (__name__)))
			return
		self.log_INFO(str("Our telegram token is '%s' and the admin id is '%s'" % (self.token, self.admin_id)))

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
		## Only answer if we are being addressed
		if ''.join([command[2], command[3]]) == metadata.handle:
			if ''.join([command[0], command[1]]) == '/help':
				self.log_CMD(str(command))
				reply = str(texts.help)
				self.log_SEND(str(reply), str(chat_id))
				self.bot.sendMessage(chat_id, reply)
			elif ''.join([command[0], command[1]]) == '/info':
				self.log_CMD(str(command))
				reply = str(texts.info)
				self.log_SEND(str(reply), str(chat_id))
				self.bot.sendMessage(chat_id, reply)
			else:
				reply = str("I'm not sure what you mean with '%s'.\nPerhaps you should try /help%s" % (' '.join(command), metadata.handle))
				self.log_SEND(str(reply), str(chat_id))
				self.bot.sendMessage(chat_id, reply)
		else:
			self.log_ERR("Don't know what to do with '%s' from %s" % (command, chat_id))
			pass
	def user_commands(self, command, chat_id):
		reply = str("I'm not sure what you mean with'%s'.\nPerhaps you should try /help" % (' '.join(command)))
		if ''.join([command[0], command[1]]) == '/help' or ''.join([[command[0], command[1], command[2], command[3]]) == ''.join(['/help', metadata.handle]):
			self.log_CMD(str(command))
			reply = str(texts.help)
		elif ''.join([command[0], command[1]]) == '/info' or ''.join([[command[0], command[1], command[2], command[3]]) == ''.join(['/info', metadata.handle]):
			self.log_CMD(str(command))
			reply = str(texts.info)
		else:
			self.log_ERR("Don't know what to do with '%s' from %s" % (command, chat_id))
			pass
		self.log_SEND(str(reply), str(chat_id))
		self.bot.sendMessage(chat_id, reply)
	def admin_commands(self, command, chat_id):
		reply = str("I'm not sure what you mean with '%s'.\nPerhaps you should try /admin" % (' '.join(command)))
		if ''.join([command[0], command[1]]) == '/help' or ''.join([[command[0], command[1], command[2], command[3]]) == ''.join(['/help', metadata.handle]):
			self.log_CMD(str(command))
			reply = str(texts.help)
		elif ''.join([command[0], command[1]]) == '/info' or ''.join([[command[0], command[1], command[2], command[3]]) == ''.join(['/info', metadata.handle]):
			self.log_CMD(str(command))
			reply = str(texts.info)
		elif ''.join([command[0], command[1]]) == '/admin' or ''.join([[command[0], command[1], command[2], command[3]]) == ''.join(['/admin', metadata.handle]):
			self.log_CMD(str(command))
			reply = str(texts.info)
		elif ''.join([command[0], command[1]]) == '/add' or ''.join([[command[0], command[1], command[2], command[3]]) == ''.join(['/add', metadata.handle]):
			pass
		elif ''.join([command[0], command[1]]) == '/del' or ''.join([[command[0], command[1], command[2], command[3]]) == ''.join(['/del', metadata.handle]):
			pass
		elif ''.join([command[0], command[1]]) == '/list' or ''.join([[command[0], command[1], command[2], command[3]]) == ''.join(['/list', metadata.handle]):
			pass
		elif ''.join([command[0], command[1]]) == '/update' or ''.join([[command[0], command[1], command[2], command[3]]) == ''.join(['/update', metadata.handle]):
			pass
		else:
			self.log_ERR("Don't know what to do with '%s' from %s" % (command, chat_id))
			pass
		try:
			self.log_SEND(str(reply), str(chat_id))
			self.bot.sendMessage(chat_id, reply)
		except Exception as e:
			self.log_ERR(str("Telegram error: %s" % (e)))
			pass

	def rcv(self, msg):
		chat_id = int(msg['chat']['id'])
		msg_text = str(msg['text'])
		## TODO: find a way to ditch all '@' but the first one
		pattern = re.compile('(^[/]{1}|[@]{1}|\w+)')
		command = re.findall(pattern, msg_text)
		
		self.log_RCV(command,str(chat_id))
		## If chat_id is negative, then we're talking with a group.
		##	therefore, we'll answer only if we're being directly addressed
		##	(command must include bot name).
		##	Otherwise, we answer any command
		if chat_id < 0:
			self.group_commands(command, str(chat_id))
		## Admin
		elif chat_id == self.admin_id:
			self.admin_commands(command,str(chat_id))
		else:
			self.user_commands(command, str(chat_id))

