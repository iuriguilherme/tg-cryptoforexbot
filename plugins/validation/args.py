# vim:fileencoding=utf-8
## Validate and test parameters
## TODO: Make all string, args, params validations here

import re

class valid():
  def __init__(self):
    pass
  def is_number(self, number):
    try:
      float(number)
      return True
    except ValueError:
      pass
    return False
  def is_safe_string(self, string):
    try:
      if string.isalpha():
        return True
    except:
      return False
    return False
  def is_safe_string_re(self, string):
    pattern = re.compile('\w+')
    try:
      valid_string = str(''.join(re.findall(pattern, string)))
      if string != '':
        return True
    except:
      return False
    return False
  def is_telegram_id(self, chat_id):
    pattern = re.compile('(-?\d+)')
    valid = ''.join(re.findall(pattern, chat_id))
    if valid != '':
      return True
    return False

