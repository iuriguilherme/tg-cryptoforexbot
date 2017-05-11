# vim:fileencoding=utf-8
## Group commands

import re
from cryptoforexbot import bot_commands, metadata, texts

class group_commands():
	def __init__(self):
		self.bot_commands = bot_commands.bot_commands()
	def parse(self, chat_id, command_list):
		## TODO: Use a better pythonic switch/case workaround
		## Only answer if we are being addressed
		## Unless it's the /conv command
		#if re.search(''.join([metadata.handle, '$']), command_list[0]):
		if command_list[0] == ''.join(['/help', metadata.handle]):
			return (True, texts.err_group[0])
		elif command_list[0] == ''.join(['/info', metadata.handle]):
			return (True, texts.err_group[0])
		elif command_list[0] == ''.join(['/list', metadata.handle]):
			return (True, texts.err_group[0])
		elif command_list[0] == ''.join(['/price', metadata.handle]):
			return (True, self.bot_commands.price(command_list))
		elif command_list[0] == '/conv' or command_list[0] == ''.join(['/conv', metadata.handle]):
			return (True, self.bot_commands.conv(command_list))
		elif re.search(''.join([metadata.handle, '$']), command_list[0]):
			return (True, str("I'm not sure what you mean with '%s'.\nPerhaps you should try /help%s" % (' '.join(command_list), metadata.handle)))
		else:
			return (False, "Don't know what to do with '%s' from %s" % (' '.join(command_list), chat_id))

