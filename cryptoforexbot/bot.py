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
from plugins.coinmarketcap import valid as coinmarketcap_valid
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
			except Exception as e:
				self.log.err("%s" % (e))
				continue

	def send(self, chat_id=0, reply='Nevermind.'):
		self.log.send(str(chat_id), str(reply))
		try:
			self.bot.sendMessage(chat_id, reply)
		except Exception as e:
			self.log.err(str("Telegram error: %s" % (e)))

	def command_conv(self, command):
		self.log.cmd(' '.join(command))
		reply = texts.err_conv[0]
		float_pattern = re.compile('[\d.]+')
		string_pattern = re.compile('\w+')
		##TODO: When things go wrong, we want to know whether it's the API fault or a code screw up
		try:
			conv_value = float(str(''.join(re.findall(float_pattern, command[1]))))
			conv_from = str(''.join(re.findall(string_pattern, command[2])))
			conv_to = str(''.join(re.findall(string_pattern, command[3])))
			reply = texts.err_conv[1]
			try:
				reply = self.coinmarketcap.conv(conv_value, conv_from, conv_to)
			except Exception as e:
				self.log.err("%s" % (e))
		except Exception as e:
			self.log.err("%s" % (e))
		return reply

	def command_list(self, command):
		self.log.cmd(' '.join(command))
		available_to = ' '.join(coinmarketcap_valid.converts)
		available_from = list()
		for c in coinmarketcap_valid.cryptos:
			available_from.append(c)
		return'Available <from> currencies: %s\n\nAvailable <to> currencies: %s' % (' '.join(available_from), available_to)

	def group_commands(self, command, chat_id):
		reply = "Nevermind."
		## Only answer if we are being addressed
		#if re.search(''.join([metadata.handle, '$']), command[0]):
		if command[0] == '/help' or command[0] == ''.join(['/help', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = texts.err_group[0]
		elif command[0] == '/info' or command[0] == ''.join(['/info', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = texts.err_group[0]
		elif command[0] == '/conv' or command[0] == ''.join(['/conv', metadata.handle]):
			reply = self.command_conv(command)
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = texts.err_group[0]
		elif re.search(''.join([metadata.handle, '$']), command[0]):
			reply = str("I'm not sure what you mean with '%s'.\nPerhaps you should try /help%s" % (' '.join(command), metadata.handle))
			self.send(chat_id, reply)
		else:
			self.log.err("Don't know what to do with '%s' from %s" % (command, chat_id))
		self.send(chat_id, reply)

	def user_commands(self, command, chat_id):
		reply = str("I'm not sure what you mean with'%s'.\nPerhaps you should try /help" % (' '.join(command)))
		if command[0] == '/help' or command[0] == ''.join(['/help', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = str(texts.help)
		elif command[0] == '/info' or command[0] == ''.join(['/info', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = str(texts.info)
		elif command[0] == '/conv' or command[0] == ''.join(['/conv', metadata.handle]):
			reply = self.command_conv(command)
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			reply = self.command_list(command)
		else:
			self.log.err("Don't know what to do with '%s' from %s" % (' '.join(command), chat_id))
			pass
		self.send(chat_id, reply)

	def admin_commands(self, command, chat_id):
		reply = str("I'm not sure what you mean with '%s'.\nPerhaps you should try /admin" % (' '.join(command)))
		if command[0] == '/help' or command[0] == ''.join(['/help', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = str(texts.help)
		elif command[0] == '/info' or command[0] == ''.join(['/info', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = str(texts.info)
		elif command[0] == '/admin' or command[0] == ''.join(['/admin', metadata.handle]):
			self.log.cmd(str(command))
			reply = str(texts.info)
		elif command[0] == '/dbadd' or command[0] == ''.join(['/dbadd', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = "Not implemented."
		elif command[0] == '/dbdel' or command[0] == ''.join(['/dbdel', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = "Not implemented."
		elif command[0] == '/dblist' or command[0] == ''.join(['/dblist', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = "Not implemented."
		elif command[0] == '/dbupdate' or command[0] == ''.join(['/dbupdate', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = "Not implemented."
		elif command[0] == '/conv' or command[0] == ''.join(['/conv', metadata.handle]):
			reply = self.command_conv(command)
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			reply = self.command_list(command)
		else:
			self.log.err("Don't know what to do with '%s' from %s" % (' '.join(command), chat_id))
		self.send(chat_id, reply)

	def rcv(self, msg):
		chat_id = int(msg['chat']['id'])
		command = list()
		for subcommand in msg['text'].split(' '):
			pattern = re.compile('(^[/]{1}|[@]{1}|[,.]|\w+)')
			item = ''.join(re.findall(pattern, subcommand))
			if item != '':
				command.append(item)

		self.log.rcv(str(chat_id), ' '.join(command))
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

