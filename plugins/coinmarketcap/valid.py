# vim:fileencoding=utf-8
## Tests for available coinmarketcap parameters (assuming our json files are updated)

import json
from cryptoforexbot import texts

class valid():
  def __init__(self):
    pass

  def crypto(self, string):
    try:
      valid_cryptos = json.load(open('plugins/coinmarketcap/cryptos.json'))
      for crypto in valid_cryptos:
        for symbol in valid_cryptos[crypto]['symbols']:
          if string.lower() == symbol.lower():
            return (True, (valid_cryptos[crypto]['coinmarketcap_id'], valid_cryptos[crypto]['name']), 'Found valid crypto: %s' % (valid_cryptos[crypto]['name']))
      return (False, texts.err_valid[0], 'Did not found crypto: %s' % (string))
    except Exception as e:
      return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))

  def convert(self, string):
    try:
      valid_converts = json.load(open('plugins/coinmarketcap/converts.json'))
      for convert in valid_converts:
        for symbol in valid_converts[convert]['symbols']:
          if string.lower() == symbol.lower():
            return (True, (valid_converts[convert]['coinmarketcap_id'], valid_converts[convert]['name']), 'Found valid convert: %s' % (valid_converts[convert]['name']))
      return (False, texts.err_valid[0], 'Did not found convert: %s' % (string))
    except Exception as e:
      return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))

  def coin(self, string):
    try:
      valid_convert = self.convert(string)
      if valid_convert[0]:
        return ('fiat', valid_convert[1], valid_convert[2])
      else:
        valid_crypto = self.crypto(string)
        if valid_crypto[0]:
          return ('crypto', valid_crypto[1], '\n'.join([valid_convert[2], valid_crypto[2]]))
        elif valid_crypto[1]:
          return (False, valid_crypto[1], valid_crypto[2])
        elif valid_crypto[2]:
          return (False, False, '\n'.join([valid_convert[2], valid_crypto[2]]))
        else:
          return (False, False, False)
    except Exception as e:
      return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))

