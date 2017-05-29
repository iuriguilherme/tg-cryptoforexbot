# vim:fileencoding=utf-8
## Group commands

import re
from cryptoforexbot import bot_commands, metadata, texts
from plugins.validation.args import valid
from plugins.coinmarketcap import valid as coinmarketcap_valid

class group_commands():
  def __init__(self):
    self.valid = valid()
    self.bot_commands = bot_commands.bot_commands()
    self.coinmarketcap_valid = coinmarketcap_valid.valid()
  def parse(self, chat_id, command_list):
    ## TODO: Use a better pythonic switch/case workaround
    ## Only answer if we are being addressed
    ## Unless it's /conv or /price
    #if re.search(''.join([metadata.handle, '$']), command_list[0]):
    if command_list[0] == ''.join(['/help', metadata.handle]):
      try:
        return (True, True, texts.err_group[0])
      except:
        return (False, True, texts.err_internal)
    elif command_list[0] == ''.join(['/info', metadata.handle]):
      try:
        return (True, True, texts.err_group[0])
      except:
        return (False, True, texts.err_internal)
    elif command_list[0] == ''.join(['/list', metadata.handle]):
      try:
        return (True, True, texts.err_group[0])
      except:
        return (False, True, texts.err_internal)
    elif command_list[0] == ''.join(['/feedback', metadata.handle]):
      try:
        return (True, True, texts.err_group[0])
      except:
        return (False, True, texts.err_internal)
    elif command_list[0] == '/price' or command_list[0] == ''.join(['/price', metadata.handle]):
      try:
        if len(command_list) == 2:
          try:
            valid_crypto = self.coinmarketcap_valid.crypto(command_list[1])
            if valid_crypto[0]:
              try:
                response = self.bot_commands.price(valid_crypto[1][0])
                if response[0]:
                  return (True, response[1], response[2])
                elif response[1]:
                  return (False, response[1], response[2])
                elif response[2]:
                  return (False, texts.err_internal, response[2])
                else:
                  return (False, False, 'DEBUG %s%sresponse: %s' % (self, '\n', response))
              except Exception as e:
                return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))
            elif valid_crypto[1]:
              return (False, valid_crypto[1], valid_crypto[2])
            elif valid_crypto[2]:
              return (False, texts.err_internal, valid_crypto[2])
            else:
              return (False, False, 'DEBUG %s%svalid_crypto: %s' % (self, '\n', valid_crypto))
          except Exception as e:
            return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))
        else:
          return (False, texts.err_param[2], 'DEBUG %s%scommand_list: %s' % (self, '\n', command_list))
      except Exception as e:
        return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))
    elif command_list[0] == '/conv' or command_list[0] == ''.join(['/conv', metadata.handle]):
      try:
        if len(command_list) == 4:
          if self.valid.is_number(command_list[1]):
            try:
              valid_crypto = self.coinmarketcap_valid.coin(command_list[2])
              if valid_crypto[0]:
                try:
                  valid_convert = self.coinmarketcap_valid.coin(command_list[3])
                  if valid_convert[0]:
                    try:
                      response = self.bot_commands.conv(command_list[1], (valid_crypto[0], valid_crypto[1]), (valid_convert[0], valid_convert[1]))
                      if response[0]:
                        return (True, response[1], response[2])
                      elif response[1]:
                        return (False, response[1], response[2])
                      elif response[2]:
                        return (False, False, response[2])
                      else:
                        return (False, False, 'DEBUG %s%sresponse: %s' % (self, '\n', response))
                        ## This identation level is also known as "python street fighter"
                        ## https://twitter.com/dr4goonis/status/476617165463105536
                    except Exception as e:
                      return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))
                  elif valid_convert[1]:
                    return (False, valid_convert[1], valid_convert[2])
                  elif valid_convert[2]:
                    return (False, False, valid_convert[2])
                  else:
                    return (False, False, 'DEBUG %s%svalid_convert: %s' % (self, '\n', valid_convert))
                except Exception as e:
                  return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))
              elif valid_crypto[1]:
                return (False, valid_crypto[1], valid_crypto[2])
              elif valid_crypto[2]:
                return (False, False, valid_crypto[2])
              else:
                return (False, False, 'DEBUG %s%svalid_crypto: %s' % (self, '\n', valid_crypto))
            except Exception as e:
              return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))
          else:
            return (False, texts.err_valid[1], 'DEBUG %s%scommand_list: %s' % (self, '\n', command_list))
        else:
          return (False, texts.err_param[1], 'DEBUG %s%scommand_list: %s' % (self, '\n', command_list))
      except Exception as e:
        return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))
    elif re.search(''.join([metadata.handle, '$']), command_list[0]):
      return (True, True, str("I'm not sure what you mean with '%s'.\nPerhaps you should try /help%s" % (' '.join(command_list), metadata.handle)))
    else:
      return (False, False, "Don't know what to do with '%s' from %s" % (' '.join(command_list), chat_id))

