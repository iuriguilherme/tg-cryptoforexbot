# vim:fileencoding=utf-8
## TODO: Debug logging

import re

from plugins.coinmarketcap.api import coinmarketcap as api
from plugins.coinmarketcap import valid
from cryptoforexbot import texts

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
				return ' '.join(["(from coinmarketcap.com):", '{:,}'.format(safe_value), safe_from, "=" , '{:,}'.format(result), safe_to])
		else:
			return texts.err_valid
		return False

	def price(self, crypto='BTC'):
		safe_crypto = crypto

		try:
			check_crypto = self.test_crypto(valid.cryptos, safe_crypto)
		except Exception as e:
			print('DEBUG: %s' % (e))
		if check_crypto:
			try:
				response = self.api.get_ticker_id(check_crypto, '')
			except Exception as e:
				print('DEBUG: %s' % (e))
			if response:
				return """
Price information for %s (from coinmarketcap.com)

1 %s equals
$ %s USD
%s BTC

Price change since last
hour:\t%s%s
day:\t%s%s
week:\t%s%s

Last 24 hours volume:\t$ %s USD
Marketcap:\t$ %s USD

Available supply:\t%s %s
Total supply:\t%s %s
""" % (response[0]['name'], response[0]['symbol'], '{:,}'.format(float(response[0]['price_usd'])), '{:,}'.format(float(response[0]['price_btc'])), response[0]['percent_change_1h'], '%', response[0]['percent_change_24h'], '%', response[0]['percent_change_7d'], '%', '{:,}'.format(float(response[0]['24h_volume_usd'])), '{:,}'.format(float(response[0]['market_cap_usd'])), '{:,}'.format(float(response[0]['available_supply'])), response[0]['symbol'], '{:,}'.format(float(response[0]['total_supply'])), response[0]['symbol'])
			else:
				return texts.err_params[0]
		else:
			return texts.err_valid
		return False

