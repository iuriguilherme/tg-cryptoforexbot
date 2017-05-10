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

from cryptoforexbot import metadata, texts, commands
from plugins.coinmarketcap.wrapper import coinmarketcap
from plugins.coinmarketcap import valid as coinmarketcap_valid
from plugins.log.stdout import stdout as log

class cryptoforex():

	def __init__(self):
		self.log = log()
		self.log.info(str("Starting %s" % (__name__)))
		self.coinmarketcap = coinmarketcap()
		self.command = commands.command()

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

	def group_commands(self, command, chat_id):
		## Only answer if we are being addressed
		#if re.search(''.join([metadata.handle, '$']), command[0]):
		if command[0] == '/help' or command[0] == ''.join(['/help', metadata.handle]):
			self.log.cmd(' '.join(command))
			self.send(chat_id, texts.err_group[0])
		elif command[0] == '/info' or command[0] == ''.join(['/info', metadata.handle]):
			self.log.cmd(' '.join(command))
			self.send(chat_id, texts.err_group[0])
		elif command[0] == '/conv' or command[0] == ''.join(['/conv', metadata.handle]):
			self.send(chat_id, self.command.conv(command))
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			self.log.cmd(' '.join(command))
			self.send(chat_id, texts.err_group[0])
		elif command[0] == '/price' or command[0] == ''.join(['/price', metadata.handle]):
			self.log.cmd(' '.join(command))
			self.send(chat_id, self.command.conv(command))
		elif re.search(''.join([metadata.handle, '$']), command[0]):
			self.send(chat_id, "I'm not sure what you mean with '%s'.\nPerhaps you should try /help%s" % (' '.join(command), metadata.handle))
		else:
			self.log.err("Don't know what to do with '%s' from %s" % (command, chat_id))

	def user_commands(self, command, chat_id):
		reply = str("I'm not sure what you mean with'%s'.\nPerhaps you should try /help" % (' '.join(command)))
		if command[0] == '/help' or command[0] == ''.join(['/help', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = str(texts.help)
		elif command[0] == '/info' or command[0] == ''.join(['/info', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = str(texts.info)
		elif command[0] == '/conv' or command[0] == ''.join(['/conv', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = self.command.conv(command)
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = self.command.list(command)
		elif command[0] == '/price' or command[0] == ''.join(['/price', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = self.command.price(command)
		else:
			self.log.err("Don't know what to do with '%s' from %s" % (' '.join(command), chat_id))
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
			self.log.cmd(' '.join(command))
			reply = self.command.conv(command)
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = self.command.list(command)
		elif command[0] == '/price' or command[0] == ''.join(['/price', metadata.handle]):
			self.log.cmd(' '.join(command))
			reply = self.command.price(command)
		elif command[0] == '/send' or command[0] == ''.join(['/send', metadata.handle]):
			self.log.cmd(' '.join(command))
			chat_id = command[1]
			reply = ' '.join(command[2::1])
		else:
			self.log.err("Don't know what to do with '%s' from %s" % (' '.join(command), chat_id))
		self.send(chat_id, reply)

	def rcv(self, msg):
		chat_id = int(msg['chat']['id'])
		command = list()
		for subcommand in msg['text'].split(' '):
			pattern = re.compile('(^[/]{1}|[@]{1}|[,.]|-?\d+|\n|\w+)')
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

