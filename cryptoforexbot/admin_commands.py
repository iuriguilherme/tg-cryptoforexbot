# vim:fileencoding=utf-8
## Admin commands

from cryptoforexbot import bot_commands, metadata, texts
from plugins.validation.args import valid

class admin_commands():
  def __init__(self):
    self.valid = valid()
    self.bot_commands = bot_commands.bot_commands()
  def parse(self, chat_id, command_list):
    ## TODO: Use a better pythonic switch/case workaround
    if command_list[0] == '/admin' or command_list[0] == ''.join(['/admin', metadata.handle]):
      try:
        return (True, True, texts.admin)
      except Exception as e:
        return(False, True, 'DEBUG %s%sexception: %s' % (self, '\n', e))
    elif command_list[0] == '/dbadd' or command_list[0] == ''.join(['/dbadd', metadata.handle]):
      try:
        return (True, True, texts.err_param[4])
      except:
        return (False, True, texts.err_internal)
    elif command_list[0] == '/dbdel' or command_list[0] == ''.join(['/dbdel', metadata.handle]):
      try:
        return (True, True, texts.err_param[4])
      except:
        return (False, True, texts.err_internal)
    elif command_list[0] == '/dblist' or command_list[0] == ''.join(['/dblist', metadata.handle]):
      try:
        return (True, True, texts.err_param[4])
      except:
        return (False, True, texts.err_internal)
    elif command_list[0] == '/dbupdate' or command_list[0] == ''.join(['/dbupdate', metadata.handle]):
      try:
        return (True, True, texts.err_param[4])
      except:
        return (False, True, texts.err_internal)
    elif command_list[0] == '/send' or command_list[0] == ''.join(['/info', metadata.handle]):
      if len(command_list) > 2:
        if self.valid.is_telegram_id(command_list[1]):
          return ('send', command_list[1], ' '.join(command_list[2::1]))
      return (True, True, texts.err_param[3])
    elif command_list[0] == '/debug' or command_list[0] == ''.join(['/debug', metadata.handle]):
      if len(command_list) > 1:
        if self.valid.is_safe_string(command_list[1]):
          response = self.bot_commands.debug(command_list[1::1])
          if response[0]:
            return (True, True, response[2])
          elif response[1]:
            return (False, True, response[2])
          elif response[2]:
            return (False, False, response[2])
          return (False, False, 'Nothing happened')
        return (False, True, 'Your params are shit')
      return (False, True, 'No param, no reply')
    else:
      print ('DEBUG? %s%schat_id: %s%scommand_list: %s' % (self, '\n', chat_id, '\n', command_list)) # TODO DEBUG
      return (False, False, False)
    return (False, False, False)

