# vim:fileencoding=utf-8
## TODO: Debug logging

import re

from plugins.coinmarketcap.api import coinmarketcap as api
from plugins.coinmarketcap import valid
from cryptoforexbot import texts

class coinmarketcap():

	def __init__(self):
		self.api = api()
		self.valid = valid.valid()

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
		try:
			response = self.api.get_ticker_id(conv_from, conv_to)
		except Exception as e:
			return (False, False, '%s' % (e))
		if response:
			result = float(float(conv_value) * float(response[0][''.join(['price_',conv_to.lower()])]))
			return (True, True, ' '.join(["(from coinmarketcap.com):", '{:,}'.format(float(conv_value)), conv_from, "=" , '{:,}'.format(float(result)), conv_to]))
		return (False, True, texts.err_internal)

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

