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

from cryptoforexbot import command, metadata, texts
from plugins.coinmarketcap.wrapper import coinmarketcap
from plugins.coinmarketcap import valid as coinmarketcap_valid
from plugins.log.log_str import log_str

class cryptoforex():

	def __init__(self):
		self.log_str = log_str()
		self.coinmarketcap = coinmarketcap()

		print(self.log_str.info("Starting %s" % (metadata.name)))
		self.config_file = str("cryptoforexbot/cryptoforexbot.cfg")
		self.config = ConfigParser.ConfigParser()
		try:
			self.config.read(self.config_file)
			self.token = str(self.config.get("botfather", "token"))
			self.admin_id = int(self.config.get("admin", "id"))
			self.group_id = int(self.config.get("admin", "group"))
		except ConfigParser.NoSectionError:
			#self.log(self.log_str.err(texts.err_config))
			print(self.log_str.err(texts.err_config))
			#self.log(self.log_str.info("Exiting %s." % (__name__)))
			print(self.log_str.info("Exiting %s" % (metadata.name)))
			return

		print(self.log_str.info("Our telegram token is '%s', the admin id is '%s' and the admin group id is '%s'" % (self.token, self.admin_id, self.group_id)))

		self.command = command.command((self.admin_id, self.group_id))

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
			if e[1] == 429:
				time.sleep(e[2]['parameters']['retry_after']+1)
				self.bot.sendMessage(self.group_id, self.log_str.send(chat_id, reply))
		try:
			self.bot.sendMessage(chat_id, reply)
		except Exception as e:
			self.bot.sendMessage(self.group_id, self.log_str.err('Telegram error: %s' % (e)))
			print(self.log_str.err('Telegram error: %s' % (e)))
			if e[1] == 429:
				time.sleep(e[2]['parameters']['retry_after']+1)
				self.bot.sendMessage(chat_id, reply)

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

		if ''.join(command_list) != '':
			response = self.command.parse(chat_id, command_list)
			if response[0]:
				if response[1]:
					self.log(self.log_str.cmd(response[4]))
					self.send(response[2], response[3])
				else:
					self.log(self.log_str.err(response[4]))
					self.send(response[2], response[3])
			elif response[1]:
				self.log(self.log_str.cmd(response[4]))
				self.send(response[1], response[2])
				## Change group_id to admin_id to send as private message
				self.send(self.group_id, response[3])
			elif response[2]:
				for response in response[3]:
					self.send(chat_id, response)
					time.sleep(1)
			elif response[3]:
				self.log(self.log_str.err(response[4]))
			elif response[4]:
				self.log(self.log_str.debug('%s' % (response[4])))
			else:
				self.log(self.log_str.debug('%s to %s failed. Response: %s' % (' '.join(command_list), chat_id, response)))

