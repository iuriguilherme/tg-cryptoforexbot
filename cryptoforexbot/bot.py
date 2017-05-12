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

from cryptoforexbot import group_commands, user_commands, admin_commands, metadata, texts
from plugins.coinmarketcap.wrapper import coinmarketcap
from plugins.coinmarketcap import valid as coinmarketcap_valid
from plugins.log.log_str import log_str

class cryptoforex():

	def __init__(self):
		self.log_str = log_str()
		self.coinmarketcap = coinmarketcap()
		self.group_commands = group_commands.group_commands()
		self.user_commands = user_commands.user_commands()
		self.admin_commands = admin_commands.admin_commands()

		print(self.log_str.info("Starting %s" % (metadata.name)))
		self.config_file = str("cryptoforexbot/cryptoforexbot.cfg")
		self.config = ConfigParser.ConfigParser()
		try:
			self.config.read(self.config_file)
			## If you replace the following line with something like
			##   self.token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
			##   , it will work too. Your code will be ugly, however.
			self.token = str(self.config.get("botfather", "token"))
			self.admin_id = int(self.config.get("admin", "id"))
			self.group_id = int(self.config.get("admin", "group"))
		except ConfigParser.NoSectionError:
			#self.log(self.log_str.err(texts.err_config))
			print(self.log_str.err(texts.err_config))
			#self.log(self.log_str.info("Exiting %s." % (__name__)))
			print(self.log_str.info("Exiting %s" % (metadata.name)))
			return
		print(self.log_str.info("Our telegram token is '%s', the admin id is '%s' and the admin group is '%s'" % (self.token, self.admin_id, self.group_id)))

		try:
			self.bot = telepot.Bot(self.token)
			self.bot.message_loop(self.rcv)
		except Exception as e:
			self.log(self.log_str.err("Telegram error: %s" % (e)))
			pass
		self.log(self.log_str.info("Started %s" % (metadata.name)))

		while 1:
			try:
				time.sleep(10)
			except KeyboardInterrupt:
				self.log(self.log_str.info("Exiting %s" % (metadata.name)))
				time.sleep(1)
				return
			except Exception as e:
				self.log(self.log_str.err("%s" % (e)))
				continue

	def send(self, chat_id=0, reply='Nevermind.'):
		try:
			if chat_id != self.group_id:
				self.bot.sendMessage(self.group_id, self.log_str.send(chat_id, reply))
		except Exception as e:
			self.bot.sendMessage(self.group_id, self.log_str.err('%s' % (e)))
			print(self.log_str.err('%s' % (e)))
		try:
			self.bot.sendMessage(chat_id, reply)
		except Exception as e:
			self.bot.sendMessage(self.group_id, self.log_str.err('Telegram error: %s' % (e)))
			print(self.log_str.err('Telegram error: %s' % (e)))

	def log(self, reply):
		print(reply)
		self.send(self.group_id, reply)

	def rcv(self, msg):
		chat_id = self.group_id
		command_list = list()
		try:
			chat_id = int(msg['chat']['id'])
			for subcommand in ' '.join(unicode(msg['text']).splitlines()).split(' '):
				pattern = re.compile(u'(^[/]{1}|[@]{1}|[,.]|-?\d+|\n|\w+)', re.UNICODE)
				item = ''.join(re.findall(pattern, subcommand))
				if item != '':
					command_list.append(item)
		except Exception as e:
			self.log(self.log_str.err('Telepot error: %s' % (e)))

		self.log(self.log_str.rcv(str(chat_id), ' '.join(command_list)))

		## TODO: From this point below, this is once more becoming too big and redundant. Need a rewrite.
		## If chat_id is negative, then we're talking with a group.
		if chat_id < 0:
			## Admin group
			if chat_id == self.group_id:
				response = self.admin_commands.parse(chat_id, command_list)
				if response[0]:
					self.log(self.log_str.cmd(' '.join(command_list)))
					if response[0] == 'send':
						self.send(response[1], response[2])
					else:
						self.send(chat_id, response[2])
				elif response[1]:
					self.log(self.log_str.err(response[2]))
				elif response[2]:
					self.log(self.log_str.debug(response[2]))
				else:
					response = self.group_commands.parse(chat_id, command_list)
					if response[0]:
						self.log(self.log_str.cmd(' '.join(command_list)))
						self.send(chat_id, response[1])
					else:
						self.log(self.log_str.err(response[1]))
			## Regular group
			else:
				response = self.group_commands.parse(chat_id, command_list)
				if response[0]:
					self.send(chat_id, response[1])
				else:
					self.log(self.log_str.err(response[1]))
		## Admin user
		elif chat_id == self.admin_id:
			response = self.admin_commands.parse(chat_id, command_list)
			if response[0]:
				self.log(self.log_str.cmd(' '.join(command_list)))
				if response[0] == 'send':
					self.send(response[1], response[2])
				else:
					self.send(chat_id, response[2])
			elif response[1]:
				self.log(self.log_str.err(response[2]))
				self.send(chat_id, response[2])
			elif response[2]:
				self.log(self.log_str.err(response[2]))
			else:
				response = self.user_commands.parse(chat_id, command_list)
				if response[0]:
					self.log(self.log_str.cmd(' '.join(command_list)))
					if response[0] == 'feedback':
						if response[1]:
							## Change group_id to admin_id to send as private message
							self.send(self.group_id, '#feedback\nUser %s sent this message as feedback:\n\n%s' % (chat_id, response[2]))
							self.send(chat_id, texts.feedback)
						else:
							self.log(self.log_str.err(response[2]))
							self.send(chat_id, response[2])
					else:
						self.send(chat_id, response[2])
				elif response[1]:
					self.log(self.log_str.err(response[2]))
					self.send(chat_id, response[2])
				elif response[2]:
					self.log(self.log_str.err(response[2]))
					self.send(chat_id, texts.err_internal)
				else:
					self.log(self.log_str.debug('%s to %s failed.' % (' '.join(command_list), chat_id)))
		## Regular user
		else:
			response = self.user_commands.parse(chat_id, command_list)
			if response[0]:
				self.log(self.log_str.cmd(' '.join(command_list)))
				if response[0] == 'feedback':
					if response[1]:
						## Change group_id to admin_id to send as private message
						self.send(self.group_id, '#feedback\nUser %s sent this message as feedback:\n\n%s' % (chat_id, response[2]))
						self.send(chat_id, texts.feedback)
					else:
						self.log(self.log_str.err(response[2]))
						self.send(chat_id, response[2])
				else:
					self.send(chat_id, response[2])
			elif response[1]:
				self.log(self.log_str.err(response[2]))
				self.send(chat_id, response[2])
			elif response[2]:
				self.log(self.log_str.err(response[2]))
				self.send(chat_id, texts.err_internal)
			else:
				self.log(self.log_str.debug('%s to %s failed.' % (' '.join(command_list), chat_id)))

