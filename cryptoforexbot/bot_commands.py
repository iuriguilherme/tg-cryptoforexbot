# vim:fileencoding=utf-8
## TODO: Debug logging

import re
import json

from cryptoforexbot import texts
from plugins.coinmarketcap.wrapper import coinmarketcap
#from plugins.coinmarketcap import valid as coinmarketcap_valid

class bot_commands():

	def __init__(self):
		self.coinmarketcap = coinmarketcap()
#		self.coinmarketcap_valid = coinmarketcap_valid.valid()

	def conv(self, conv_value, conv_from, conv_to):
		try:
			response = self.coinmarketcap.conv(conv_value, conv_from, conv_to)
			if response[0]:
				return (True, True, response[2])
			elif response[1]:
				return (False, True, response[2])
			elif response[2]:
				return (False, False, response[2])
			else:
				return (False, True, texts.err_internal)
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, True, texts.err_internal)

	def list(self):
		## TODO: Treat json exceptions, use three arguments for return
		try:
			cryptos_dict = json.load(open('plugins/coinmarketcap/cryptos.json'))
			converts_dict = json.load(open('plugins/coinmarketcap/converts.json'))

			reply = list()
			reply.append("Symbols are case insensitive. Currently we only support converting from cryptocurrencies to fiat currencies available at coinmarketcap.")
			reply.append('')
			reply.append('')

			reply_from = list()
			reply_from.append("Supported currencies you can convert <from>:")
			reply_from.append('')

			reply_from_currencies = list()
			for crypto in cryptos_dict:
				reply_from_currencies.append(''.join([cryptos_dict[crypto]['name'], ' - symbol can be any of: ']))
				reply_from_currencies_symbols = list()
				for symbol in cryptos_dict[crypto]['symbols']:
					reply_from_currencies_symbols.append(symbol)
				reply_from_currencies.append(''.join(['(', ', '.join(reply_from_currencies_symbols), ')']))
				reply_from_currencies.append('\n')
			reply_from.append(''.join(reply_from_currencies))

			reply.append('\n'.join(reply_from))
			reply.append('')

			reply_to = list()
			reply_to.append("Supported currencies you can convert <to>:")
			reply_to.append('')

			reply_to_currencies = list()
			for convert in converts_dict:
				reply_to_currencies.append(''.join(convert))
				reply_to_currencies.append('\n')
			reply_to.append(''.join(reply_to_currencies))

			reply.append('\n'.join(reply_to))

			return (True, '\n'.join(reply))
		except Exception:
			return (False, texts.err_internal)

	def price(self, command=[]):
		print(' '.join(['DEBUG:', ' '.join(command)]))
		reply = texts.err_param[2]
		string_pattern = re.compile('\w+')
		##TODO: When things go wrong, we want to know whether it's the API fault or a code screw up
		try:
			crypto = str(''.join(re.findall(string_pattern, command[1])))
			reply = texts.err_param[0]
			try:
				reply = self.coinmarketcap.price(crypto)
			except Exception as e:
				print("DEBUG: %s" % (e))
		except Exception as e:
			print("DEBUG: %s" % (e))
		return reply

	def debug(self, param):
#		try:
#			response = self.coinmarketcap_valid.convert(param)
#			if response[0]:
#				return (True, True, response[2])
#			elif response[1]:
#				return (False, True, response[2])
#			elif response[2]:
#				return (False, False, response[2])
#			return (False, False, False)
#		except Exception as e:
#			return (False, False, '%s' % (e))
		return (False, False, False)

