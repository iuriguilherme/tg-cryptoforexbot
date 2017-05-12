# vim:fileencoding=utf-8

from cryptoforexbot import texts
from plugins.coinmarketcap.api import coinmarketcap as api

class coinmarketcap():

	def __init__(self):
		self.api = api()

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
		try:
			response = self.api.get_ticker_id(crypto, '')
		except Exception as e:
			return (False, False, '%s' % (e))
		if response:
			return (True, True, """
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
""" % (response[0]['name'], response[0]['symbol'], '{:,}'.format(float(response[0]['price_usd'])), '{:,}'.format(float(response[0]['price_btc'])), response[0]['percent_change_1h'], '%', response[0]['percent_change_24h'], '%', response[0]['percent_change_7d'], '%', '{:,}'.format(float(response[0]['24h_volume_usd'])), '{:,}'.format(float(response[0]['market_cap_usd'])), '{:,}'.format(float(response[0]['available_supply'])), response[0]['symbol'], '{:,}'.format(float(response[0]['total_supply'])), response[0]['symbol']))
		else:
			return (False, True, texts.err_internal)
		return (False, False, False)

