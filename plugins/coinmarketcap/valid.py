# vim:fileencoding=utf-8
## Tests for available coinmarketcap parameters (assuming our json files are updated)

import json

class valid():
	def __init__(self):
		pass
	def crypto(self, string):
		try:
			valid_cryptos = json.load(open('plugins/coinmarketcap/cryptos.json'))
			for crypto in valid_cryptos:
				for symbol in valid_cryptos[crypto]['symbols']:
					if string.lower() == symbol:
						return (True, True, valid_cryptos[crypto]['coinmarketcap_id'])
			return (False, True, "Unsupported crypto")
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, False, False)
	def convert(self, string):
		try:
			valid_converts = json.load(open('plugins/coinmarketcap/converts.json'))
			for convert in valid_converts:
				if string.lower() == convert.lower():
					return (True, True, convert)
			return (False, True, "Unsupported fiat")
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, False, False)

