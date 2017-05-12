# vim:fileencoding=utf-8
## User commands

import re
from cryptoforexbot import bot_commands, metadata, texts
#from plugins.log.log_str import log_str
from plugins.validation.args import valid
from plugins.coinmarketcap import valid as coinmarketcap_valid

class user_commands():
	def __init__(self):
#		self.log_str = log_str()
		self.valid = valid()
		self.bot_commands = bot_commands.bot_commands()
		self.coinmarketcap_valid = coinmarketcap_valid.valid()
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
				try:
					if len(command_list) == 4:
						if self.valid.is_number(command_list[1]):
							valid_crypto = self.coinmarketcap_valid.crypto(command_list[2])
							if valid_crypto:
								valid_convert = self.coinmarketcap_valid.convert(command_list[3])
								if valid_convert:
									try:
										response = self.bot_commands.conv(command_list[1], valid_crypto[2], valid_convert[2])
										if response[0]:
											return (True, True, response[2])
										elif response[1]:
											return (False, True, response[2])
										elif response[2]:
											return (False, False, response[2])
										else:
											return (False, False, False)
											## This identation level is also known as "python street fighter"
											## https://twitter.com/dr4goonis/status/476617165463105536
									except Exception as e:
										return (False, False, '%s' % (e))
									return (False, True, texts.err_internal)
								else:
									return (False, True, texts.err_valid[0])
							else:
								return (False, True, texts.err_valid[0])
						else:
							return (False, True, texts.err_valid[1])
					else:
						return (False, True, texts.err_param[1])
					return (False, False, False)
				except Exception as e:
					return (False, False, '%s' % (e))
				return (False, True, texts.err_internal)
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
						return ('feedback', False, texts.err_param[5])
					return (False, False, False)
				except Exception as e:
					return (False, False, '%s' % (e))
				return (False, False, False)
			else:
				return (True, True, str("I'm not sure what you mean with '%s'.\nPerhaps you should try /help" % (' '.join(command_list))))
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, False, False)

