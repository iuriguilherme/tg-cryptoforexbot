# vim:fileencoding=utf-8
## Admin commands

from cryptoforexbot import metadata, texts
from plugins.validation.args import valid

class admin_commands():
	def __init__(self):
		self.valid = valid()
	def parse(self, chat_id, command_list):
		## TODO: Use a better pythonic switch/case workaround
		if command_list[0] == '/admin' or command_list[0] == ''.join(['/admin', metadata.handle]):
			try:
				return (True, True, texts.admin)
			except Exception as e:
				return(False, True, '%s' % (e))
		elif command_list[0] == '/dbadd' or command_list[0] == ''.join(['/dbadd', metadata.handle]):
			return (True, True, texts.err_param[4])
		elif command_list[0] == '/dbdel' or command_list[0] == ''.join(['/dbdel', metadata.handle]):
			return (True, True, texts.err_param[4])
		elif command_list[0] == '/dblist' or command_list[0] == ''.join(['/dblist', metadata.handle]):
			return (True, True, texts.err_param[4])
		elif command_list[0] == '/dbupdate' or command_list[0] == ''.join(['/dbupdate', metadata.handle]):
			return (True, True, texts.err_param[4])
		elif command_list[0] == '/send' or command_list[0] == ''.join(['/info', metadata.handle]):
			if len(command_list) > 2:
				if self.valid.is_telegram_id(command_list[1]):
					return ('send', command_list[1], ' '.join(command_list[2::1]))
			return(True, True, texts.err_param[3])
		else:
			#return (True, True, str("I'm not sure what you mean with '%s'.\nPerhaps you should try /admin" % (' '.join(command_list))))
			return(False, False, False)

