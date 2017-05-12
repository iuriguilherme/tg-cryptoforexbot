# vim:fileencoding=utf-8

from cryptoforexbot import texts
from plugins.coinmarketcap.api import coinmarketcap as api

class coinmarketcap():

	def __init__(self):
		self.api = api()

	def conv(self, conv_from='BTC', conv_to='USD'):
		try:
			response = self.api.get_ticker_id(conv_from, conv_to)
		except Exception as e:
			return (False, False, '%s' % (e))
		if response:
			return (True, True, response)
		return (False, True, texts.err_internal)

	def price(self, crypto='BTC'):
		try:
			response = self.api.get_ticker_id(crypto, '')
		except Exception as e:
			return (False, False, '%s' % (e))
		if response:
			return (True, True, response)
		else:
			return (False, True, texts.err_internal)
		return (False, False, False)

