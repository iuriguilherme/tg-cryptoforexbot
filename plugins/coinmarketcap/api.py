# vim:fileencoding=utf-8
## Coinmarketcap API documented at https://coinmarketcap.com/api/
## Requests documentation at http://docs.python-requests.org/en/latest

import requests
from cryptoforexbot import metadata

class coinmarketcap():

	def __init__(self):
		self.api_url = 'https://api.coinmarketcap.com/v1/'
		self.agent = str('/'.join([metadata.agent, metadata.version]))
		self.headers = {'user-agent': self.agent}

	def __get(self, url, params={'':''}):
		safe_url = url
		request_url = ''.join([self.api_url, safe_url])
		## TODO: catch exceptions
		try:
			response = requests.get(request_url, headers=self.headers, params=params)
		except requests.exceptions.RequestException as e:
			print (e)
			return False
		if response.status_code == requests.codes.ok:
			return_message = response.json()
		else:
			return False
		return return_message

	def get_ticker(self, limit=0, convert=''):
		safe_limit = limit
		safe_convert = convert
		url = 'ticker/'
		params = {'limit' : safe_limit, 'convert': safe_convert}
		return self.__get(url, params)

	def get_ticker_id(self, currency='bitcoin', convert=''):
		safe_currency = currency
		safe_convert = convert
		url = ''.join(['ticker/', safe_currency, '/'])
		params = {'convert': safe_convert}
		return self.__get(url, params)

	def get_global(self, convert):
		safe_convert = convert
		url = 'global/'
		params = {'convert': safe_convert}
		return self.__get(url, params)

