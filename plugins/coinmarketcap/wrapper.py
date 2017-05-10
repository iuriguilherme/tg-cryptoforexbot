# vim:fileencoding=utf-8

import re

from plugins.coinmarketcap.api import coinmarketcap as api
from plugins.coinmarketcap import valid

class coinmarketcap():

	def __init__(self):
		self.api = api()

	def test_crypto(self, d, t):
		for l in d:
			for s in d[l]:
				if t in s:
					return l
		return False

	def test_convert(self, l, t):
		for s in l:
			if t in s:
				return s
		return False

	def conv(self, conv_value=0.0, conv_from='BTC', conv_to='USD'):
		safe_value = conv_value
		safe_from = conv_from
		safe_to = conv_to

		check_from = self.test_crypto(valid.cryptos, safe_from)
		check_to = self.test_convert(valid.converts, safe_to)
		if check_from and check_to:
			response = self.api.get_ticker_id(check_from, check_to)
			if response:
				result = float(float(safe_value) * float(response[0][''.join(['price_',check_to.lower()])]))
				return ''.join(["(from coinmarketcap.com): ", str(safe_value), " ", safe_from, " = " , str(result), " ", safe_to])
		return False

