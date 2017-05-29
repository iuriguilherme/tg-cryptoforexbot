# vim:fileencoding=utf-8

from cryptoforexbot import texts, user_commands, group_commands, admin_commands

class command():
  def __init__(self, (admin_id, group_id)):
    self.admin_id = admin_id
    self.group_id = group_id
    self.group_commands = group_commands.group_commands()
    self.user_commands = user_commands.user_commands()
    self.admin_commands = admin_commands.admin_commands()

  def user_parse(self, chat_id, from_id, command_list):
    response = self.user_commands.parse(chat_id, from_id, command_list)
    if response[0]:
      if response[0] == 'feedback':
        if response[1]:
          return (False, chat_id, texts.feedback, '#feedback\nUser %s sent this message as feedback:\n\n%s' % (chat_id, response[2]), ' '.join(command_list))
        else:
          return (True, False, chat_id, response[1], response[2])
      elif response[0] == 'list':
        if response[1]:
          return (False, False, chat_id, response[2], response[2])
        else:
          return (True, False, chat_id, response[1], response[2])
      else:
        return (True, True, chat_id, response[1], response[2])
    elif response[1]:
      return (True, False, chat_id, response[1], response[2])
    elif response[2]:
        return (True, False, chat_id, texts.err_internal, response[2])
    else:
      return (False, False, False, True, 'DEBUG %s%sresponse: %s' % (self, '\n', response))

  def group_parse(self, chat_id, from_id, command_list):
    response = self.group_commands.parse(chat_id, from_id, command_list)
    if response[0]:
      if response[0] == 'feedback':
        if response[1]:
          return (False, response[3], texts.feedback, '#feedback\nUser %s from group %s sent this message as feedback:\n\n%s' % (from_id, chat_id, response[2]), ' '.join(command_list))
        else:
          return (True, False, response[3], response[1], response[2])
      elif response[0] == 'list':
        if response[1]:
          return (False, False, response[3], response[2], response[2])
        else:
          return (True, False, response[3], response[1], response[2])
      else:
        return (True, True, response[3], response[1], response[2])
    elif response[1]:
      return (True, False, response[3], response[1], response[2])
    elif response[2]:
      return (False, False, False, response[3], response[2])
    elif response[3]:
      return (False, False, False, response[3], 'DEBUG %s%sresponse: %s' % (self, '\n', response))
    else:
      return (False, False, False, False, 'DEBUG %s%sresponse: %s' % (self, '\n', response))

  def admin_user_parse(self, chat_id, from_id, command_list):
    response = self.admin_commands.parse(chat_id, from_id, command_list)
    if response[0]:
      if response[0] == 'send':
        return (True, True, response[1], response[2], response[2])
      else:
        return (True, True, chat_id, response[2], response[2])
    elif response[1]:
      return (True, False, chat_id, response[2], response[2])
    elif response[2]:
      return (False, False, False, True, response[2])
    else:
      return self.user_parse(chat_id, from_id, command_list)

  def admin_group_parse(self, chat_id, from_id, command_list):
    response = self.admin_commands.parse(chat_id, from_id, command_list)
    if response[0]:
      if response[0] == 'send':
        return (True, True, response[3], response[1], response[2])
      else:
        return (True, True, response[3], response[1], response[2])
    elif response[1]:
      return (True, False, response[3], response[1], response[2])
    elif response[2]:
      return (False, False, False, response[3], response[2])
    elif response[3]:
      return self.group_parse(chat_id, from_id, command_list)
    else:
      return self.group_parse(chat_id, from_id, command_list)

  def parse(self, chat_id, from_id, command_list):
    ## If chat_id is negative, then we're talking with a group.
    if chat_id < 0:
      ## Admin group
      if chat_id == self.group_id:
        return self.admin_group_parse(chat_id, from_id, command_list)
      ## Regular group
      else:
        return self.group_parse(chat_id, from_id, command_list)
    ## Admin user
    elif chat_id == self.admin_id:
      return self.admin_user_parse(chat_id, from_id, command_list)
    ## Regular user
    else:
      return self.user_parse(chat_id, from_id, command_list)

