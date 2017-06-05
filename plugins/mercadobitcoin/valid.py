# vim:fileencoding=utf-8
## Tests for available mercadobitcoin parameters (assuming our json files are updated)

import json
from cryptoforexbot import texts

class valid():
  def __init__(self):
    pass

  def crypto(self, string):
    try:
      valid_cryptos = json.load(open('plugins/mercadobitcoin/cryptos.json'))
      for crypto in valid_cryptos:
        for symbol in valid_cryptos[crypto]['symbols']:
          if string.lower() == symbol.lower():
            return (True, (valid_cryptos[crypto]['coinmarketcap_id'], valid_cryptos[crypto]['name']), 'Found valid crypto: %s' % (valid_cryptos[crypto]['name']))
      return (False, texts.err_valid[0], 'Did not found crypto %s at mercadobitcoin.com.br' % (string))
    except Exception as e:
      return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))

  def fiat(self, string):
    try:
      valid_fiats = json.load(open('plugins/mercadobitcoin/fiat.json'))
      for fiat in valid_fiats:
        for symbol in valid_fiats[fiat]['symbols']:
          if string.lower() == symbol.lower():
            return (True, (valid_fiats[fiat]['coinmarketcap_id'], valid_fiats[fiat]['name']), 'Found valid fiat: %s' % (valid_fiats[fiat]['name']))
      return (False, texts.err_valid[0], 'Did not found fiat %s at mercadobitcoin.com.br' % (string))
    except Exception as e:
      return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))

  def coin(self, string):
    try:
      valid_crypto = self.crypto(string)
      if valid_crypto[0]:
        return ('crypto', valid_crypto[1], valid_crypto[2])
      elif valid_crypto[1]:
        return (False, valid_crypto[1], valid_crypto[2])
      elif valid_crypto[2]:
        return (False, False, 'DEBUG %s%sresponse: %s' % (self, '\n', valid_crypto[2]))
      else:
        return (False, False, False)
    except Exception as e:
      return (False, False, 'DEBUG %s%sexception: %s' % (self, '\n', e))

