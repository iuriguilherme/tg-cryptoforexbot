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
						return (True, True, (valid_cryptos[crypto]['coinmarketcap_id'], valid_cryptos[crypto]['name']))
			return (False, True, "Unsupported crypto")
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, False, False)
	def convert(self, string):
		try:
			valid_converts = json.load(open('plugins/coinmarketcap/converts.json'))
			for convert in valid_converts:
				for symbol in valid_converts[convert]['symbols']:
					if string.lower() == symbol.lower():
						return (True, True, (valid_converts[convert]['coinmarketcap_id'], valid_converts[convert]['name']))
			return (False, True, "Unsupported fiat")
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, False, False)
	def coin(self, string):
		try:
			valid_convert = self.convert(string)
			if valid_convert[0]:
				return (True, 'fiat', valid_convert[2])
			elif valid_convert[1]:
				valid_crypto = self.crypto(string)
				if valid_crypto[0]:
					return (True, 'crypto', valid_crypto[2])
				elif valid_crypto[1]:
					return (False, True, texts.err_valid[0])
				elif valid_crypto[2]:
					return (False, False, valid_crypto[2])
				else:
					return (False, False, False)
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, False, False)

