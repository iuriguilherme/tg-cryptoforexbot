# vim:fileencoding=utf-8

from cryptoforexbot import texts
from plugins.coinmarketcap.api import v1 as api

class coinmarketcap():
  def __init__(self):
    self.api = api()

  def conv(self, conv_from='BTC', conv_to='USD'):
    try:
      response = self.api.get_ticker_id(conv_from, conv_to)
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

  def price(self, crypto='BTC'):
    try:
      response = self.api.get_ticker_id(crypto, '')
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

