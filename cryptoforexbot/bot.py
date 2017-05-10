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
from plugins.log.log_str import log_str

class cryptoforex():

	def __init__(self):
		self.log_str = log_str()
		self.coinmarketcap = coinmarketcap()
		self.command = commands.command()

		print(self.log_str.info("Starting %s" % (__name__)))
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
			print(self.log_str.info("Exiting %s." % (__name__)))
			return
		print(self.log_str.info("Our telegram token is '%s', the admin id is '%s' and the admin group is '%s'" % (self.token, self.admin_id, self.group_id)))

		try:
			self.bot = telepot.Bot(self.token)
			self.bot.message_loop(self.rcv)
		except Exception as e:
			self.log(self.log_str.err("Telegram error: %s" % (e)))
			pass

		while 1:
			try:
				time.sleep(10)
			except KeyboardInterrupt:
				self.log(self.log_str.info("Exiting %s." % (__name__)))
				return
			except Exception as e:
				self.log(self.log_str.err("%s" % (e)))
				continue

	def send(self, chat_id=0, reply='Nevermind.'):
		print(self.log_str.send(str(chat_id), str(reply)))
		try:
			self.bot.sendMessage(chat_id, reply)
		except Exception as e:
			print(self.log_str.err(str("Telegram error: %s" % (e))))
			pass

	def log(self, reply):
		print(reply)
		self.send(self.group_id, reply)

	def group_commands(self, chat_id, command):
		## Only answer if we are being addressed
		#if re.search(''.join([metadata.handle, '$']), command[0]):
		if command[0] == '/help' or command[0] == ''.join(['/help', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			self.send(chat_id, texts.err_group[0])
		elif command[0] == '/info' or command[0] == ''.join(['/info', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			self.send(chat_id, texts.err_group[0])
		elif command[0] == '/conv' or command[0] == ''.join(['/conv', metadata.handle]):
			self.send(chat_id, self.command.conv(command))
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			self.send(chat_id, texts.err_group[0])
		elif command[0] == '/price' or command[0] == ''.join(['/price', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			self.send(chat_id, self.command.conv(command))
		elif re.search(''.join([metadata.handle, '$']), command[0]):
			self.send(chat_id, "I'm not sure what you mean with '%s'.\nPerhaps you should try /help%s" % (' '.join(command), metadata.handle))
		else:
			self.log(self.log_str.err("Don't know what to do with '%s' from %s" % (command, chat_id)))

	def user_commands(self, chat_id, command):
		reply = str("I'm not sure what you mean with'%s'.\nPerhaps you should try /help" % (' '.join(command)))
		if command[0] == '/help' or command[0] == ''.join(['/help', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = str(texts.help)
		elif command[0] == '/info' or command[0] == ''.join(['/info', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = str(texts.info)
		elif command[0] == '/conv' or command[0] == ''.join(['/conv', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = self.command.conv(command)
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = self.command.list(command)
		elif command[0] == '/price' or command[0] == ''.join(['/price', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = self.command.price(command)
		else:
			self.log(self.log_str.err("Don't know what to do with '%s' from %s" % (' '.join(command), chat_id)))
		self.send(chat_id, reply)

	def admin_commands(self, chat_id, command):
		reply = str("I'm not sure what you mean with '%s'.\nPerhaps you should try /admin" % (' '.join(command)))
		if command[0] == '/help' or command[0] == ''.join(['/help', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = str(texts.help)
		elif command[0] == '/info' or command[0] == ''.join(['/info', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = str(texts.info)
		elif command[0] == '/admin' or command[0] == ''.join(['/admin', metadata.handle]):
			self.log(self.log_str.cmd(str(command)))
			reply = str(texts.info)
		elif command[0] == '/dbadd' or command[0] == ''.join(['/dbadd', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = "Not implemented."
		elif command[0] == '/dbdel' or command[0] == ''.join(['/dbdel', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = "Not implemented."
		elif command[0] == '/dblist' or command[0] == ''.join(['/dblist', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = "Not implemented."
		elif command[0] == '/dbupdate' or command[0] == ''.join(['/dbupdate', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = "Not implemented."
		elif command[0] == '/conv' or command[0] == ''.join(['/conv', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = self.command.conv(command)
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = self.command.list(command)
		elif command[0] == '/price' or command[0] == ''.join(['/price', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = self.command.price(command)
		elif command[0] == '/send' or command[0] == ''.join(['/send', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			chat_id = command[1]
			reply = ' '.join(command[2::1])
		else:
			self.log(self.log_str.err("Don't know what to do with '%s' from %s" % (' '.join(command), chat_id)))
		self.send(chat_id, reply)

	def admin_group_commands(self, chat_id, command):
		reply = str("I'm not sure what you mean with '%s'.\nPerhaps you should try /admin" % (' '.join(command)))
		if command[0] == '/help' or command[0] == ''.join(['/help', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = str(texts.help)
		elif command[0] == '/info' or command[0] == ''.join(['/info', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = str(texts.info)
		elif command[0] == '/admin' or command[0] == ''.join(['/admin', metadata.handle]):
			self.log(self.log_str.cmd(str(command)))
			reply = str(texts.info)
		elif command[0] == '/dbadd' or command[0] == ''.join(['/dbadd', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = "Not implemented."
		elif command[0] == '/dbdel' or command[0] == ''.join(['/dbdel', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = "Not implemented."
		elif command[0] == '/dblist' or command[0] == ''.join(['/dblist', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = "Not implemented."
		elif command[0] == '/dbupdate' or command[0] == ''.join(['/dbupdate', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = "Not implemented."
		elif command[0] == '/conv' or command[0] == ''.join(['/conv', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = self.command.conv(command)
		elif command[0] == '/list' or command[0] == ''.join(['/list', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = self.command.list(command)
		elif command[0] == '/price' or command[0] == ''.join(['/price', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			reply = self.command.price(command)
		elif command[0] == '/send' or command[0] == ''.join(['/send', metadata.handle]):
			self.log(self.log_str.cmd(' '.join(command)))
			chat_id = command[1]
			reply = ' '.join(command[2::1])
		else:
			self.log(self.log_str.err("Don't know what to do with '%s' from %s" % (' '.join(command), chat_id)))
		self.send(chat_id, reply)

	def rcv(self, msg):
		chat_id = self.group_id
		command = list()
		try:
			chat_id = int(msg['chat']['id'])
			for subcommand in msg['text'].split(' '):
				pattern = re.compile('(^[/]{1}|[@]{1}|[,.]|-?\d+|\n|\w+)')
				item = ''.join(re.findall(pattern, subcommand))
				if item != '':
					command.append(item)
		except Exception as e:
			self.log(self.log_str.err('Telepot error: %s' % (e)))

		self.log(self.log_str.rcv(str(chat_id), ' '.join(command)))
		## If chat_id is negative, then we're talking with a group.
		if chat_id < 0:
			## Group admin
			if chat_id == self.group_id:
				self.admin_group_commands(str(chat_id), command)
			else:
				self.group_commands(str(chat_id), command)
		## Admin
		elif chat_id == self.admin_id:
			self.admin_commands(str(chat_id), command)
		else:
			self.user_commands(str(chat_id), command)

