# vim:fileencoding=utf-8
## User commands

import re
from cryptoforexbot import bot_commands, metadata, texts
from plugins.log.log_str import log_str

class user_commands():
	def __init__(self):
		self.log_str = log_str()
		self.bot_commands = bot_commands.bot_commands()
	def parse(self, chat_id, command_list):
		try:
			## TODO: Use a better pythonic switch/case workaround
			if command_list[0] == '/start' or command_list[0] == ''.join(['/start', metadata.handle]):
				return (True, True, texts.help)
			elif command_list[0] == '/help' or command_list[0] == ''.join(['/help', metadata.handle]):
				return (True, True, texts.help)
			elif command_list[0] == '/info' or command_list[0] == ''.join(['/info', metadata.handle]):
				return (True, True, texts.info)
			elif command_list[0] == '/conv' or command_list[0] == ''.join(['/conv', metadata.handle]):
				return (True, True, self.bot_commands.conv(command_list))
			elif command_list[0] == '/price' or command_list[0] == ''.join(['/price', metadata.handle]):
				return (True, True, self.bot_commands.price(command_list))
			elif command_list[0] == '/list' or command_list[0] == ''.join(['/list', metadata.handle]):
				response = self.bot_commands.list()
				if response[0]:
					return (True, True, response[1])
				return (False, True, texts.err_internal)
			elif command_list[0] == '/feedback' or command_list[0] == ''.join(['/feedback', metadata.handle]):
				try:
					if len(command_list) > 1:
						return ('feedback', True, ' '.join(command_list[1::1]))
					else:
						return (False, True, texts.err_param[5])
					return (False, False, False)
				except Exception as e:
					return (False, False, '%s' % (e))
				return (False, False, False)
			else:
				return (True, True, str("I'm not sure what you mean with '%s'.\nPerhaps you should try /help" % (' '.join(command_list))))
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, False, False)

