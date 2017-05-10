# vim:fileencoding=utf-8
## Telegram bots documentation at https://core.telegram.org/bots
## Telepot documentation at https://telepot.readthedocs.io/en/latest/

import re
import time
import ConfigParser

try:
	import telepot
except (ImportError, NameError):
	print "You have to `pip install telepot`. Try again when you do."
	exit()

from cryptoforexbot import metadata, texts
from plugins.coinmarketcap.wrapper import coinmarketcap
from plugins.log.stdout import stdout as log

class cryptoforex():

	def __init__(self):
		self.log = log()
		self.log.info(str("Starting %s" % (__name__)))
		self.coinmarketcap = coinmarketcap()

		self.config_file = str("cryptoforexbot/cryptoforexbot.cfg")
		self.log.info(str("Opening config file: %s" % (self.config_file)))
		self.config = ConfigParser.ConfigParser()
		try:
			self.config.read(self.config_file)
			## If you replace the following line with something like
			##   self.token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
			##   , it will work too. Your code will be ugly, however.
			self.token = str(self.config.get("botfather", "token"))
			self.admin_id = int(self.config.get("admin", "id"))
		except ConfigParser.NoSectionError:
			self.log.err(str(texts.err_config))
			self.log.info(str("Exiting %s." % (__name__)))
			return
		self.log.info(str("Our telegram token is '%s' and the admin id is '%s'" % (self.token, self.admin_id)))

		try:
			self.bot = telepot.Bot(self.token)
			self.bot.message_loop(self.rcv)
		except Exception as e:
			self.log.err(str("Telegram error: %s" % (e)))
			pass

		while 1:
			try:
				time.sleep(10)
			except KeyboardInterrupt:
				self.log.info(str("Exiting %s." % (__name__)))
				return

	def group_commands(self, command, chat_id):
		reply = str()
		## Only answer if we are being addressed
		if ''.join([command[2], command[3]]) == metadata.handle:
			if ''.join([command[0], command[1]]) == '/help':
				self.log.cmd(str(command))
				reply = str(texts.help)
				self.log.send(str(reply), str(chat_id))
				self.bot.sendMessage(chat_id, reply)
			elif ''.join([command[0], command[1]]) == '/info':
				self.log.cmd(str(command))
				reply = str(texts.info)
				self.log.send(str(reply), str(chat_id))
				self.bot.sendMessage(chat_id, reply)
			else:
				reply = str("I'm not sure what you mean with '%s'.\nPerhaps you should try /help%s" % (' '.join(command), metadata.handle))
				self.log.send(str(reply), str(chat_id))
				self.bot.sendMessage(chat_id, reply)
		else:
			self.log.err("Don't know what to do with '%s' from %s" % (command, chat_id))
			pass
	def user_commands(self, command, chat_id):
		reply = str("I'm not sure what you mean with'%s'.\nPerhaps you should try /help" % (' '.join(command)))
		if ''.join([command[0], command[1]]) == '/help' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/help', metadata.handle]):
			self.log.cmd(str(command))
			reply = str(texts.help)
		elif ''.join([command[0], command[1]]) == '/info' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/info', metadata.handle]):
			self.log.cmd(str(command))
			reply = str(texts.info)
		else:
			self.log.err("Don't know what to do with '%s' from %s" % (command, chat_id))
			pass
		self.log.send(str(reply), str(chat_id))
		self.bot.sendMessage(chat_id, reply)
	def admin_commands(self, command, chat_id):
		reply = str("I'm not sure what you mean with '%s'.\nPerhaps you should try /admin" % (' '.join(command)))
		if ''.join([command[0], command[1]]) == '/help' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/help', metadata.handle]):
			self.log.cmd(str(command))
			reply = str(texts.help)
		elif ''.join([command[0], command[1]]) == '/info' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/info', metadata.handle]):
			self.log.cmd(str(command))
			reply = str(texts.info)
		elif ''.join([command[0], command[1]]) == '/admin' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/admin', metadata.handle]):
			self.log.cmd(str(command))
			reply = str(texts.info)
		elif ''.join([command[0], command[1]]) == '/add' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/add', metadata.handle]):
			pass
		elif ''.join([command[0], command[1]]) == '/del' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/del', metadata.handle]):
			pass
		elif ''.join([command[0], command[1]]) == '/list' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/list', metadata.handle]):
			pass
		elif ''.join([command[0], command[1]]) == '/update' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/update', metadata.handle]):
			pass
		elif ''.join([command[0], command[1]]) == '/conv' or ''.join([command[0], command[1], command[2], command[3]]) == ''.join(['/conv', metadata.handle]):
			self.log.cmd(str(command))
			reply = texts.err_conv[0]
			float_pattern = re.compile('[\d,.]+')
			string_pattern = re.compile('\w+')
			##TODO: When things go wrong, we want to know whether it's the API fault or a code screw up
			try:
				if command[2] == '@':
					conv_value = float(''.join(re.findall(float_pattern, command[4])))
					conv_from = str(''.join(re.findall(string_pattern, command[5])))
					conv_to = str(''.join(re.findall(string_pattern, command[6])))
				else:
					conv_value = float(''.join(re.findall(float_pattern, command[2])))
					conv_from = str(''.join(re.findall(string_pattern, command[3])))
					conv_to = str(''.join(re.findall(string_pattern, command[4])))
				reply = texts.err_conv[1]
				try:
					reply = self.coinmarketcap.conv(conv_value, conv_from, conv_to)
				except Exception as e:
					self.log.err("%s" % (e))
			except Exception as e:
				self.log.err("%s" % (e))
		else:
			self.log.err("Don't know what to do with '%s' from %s" % (command, chat_id))
		try:
			self.log.send(str(reply), str(chat_id))
			self.bot.sendMessage(chat_id, reply)
		except Exception as e:
			self.log.err(str("Telegram error: %s" % (e)))
			pass

	def rcv(self, msg):
		chat_id = int(msg['chat']['id'])
		msg_text = str(msg['text'])
		## TODO: find a way to ditch all '@' but the first one
		pattern = re.compile('(^[/]{1}|[@]{1}|\w+)')
		command = re.findall(pattern, msg_text)
		
		self.log.rcv(command,str(chat_id))
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

