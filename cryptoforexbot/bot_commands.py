# vim:fileencoding=utf-8
## TODO: Debug logging

import re

from cryptoforexbot import texts
from plugins.coinmarketcap.wrapper import coinmarketcap
from plugins.coinmarketcap import valid as coinmarketcap_valid

class bot_commands():

	def __init__(self):
		self.coinmarketcap = coinmarketcap()

	def conv(self, command=[]):
		print(' '.join(['DEBUG:', ' '.join(command)]))
		reply = texts.err_param[1]
		float_pattern = re.compile('[\d.]+')
		string_pattern = re.compile('\w+')
		##TODO: When things go wrong, we want to know whether it's the API fault or a code screw up
		try:
			conv_value = float(str(''.join(re.findall(float_pattern, command[1]))))
			conv_from = str(''.join(re.findall(string_pattern, command[2])))
			conv_to = str(''.join(re.findall(string_pattern, command[3])))
			reply = texts.err_param[0]
			try:
				reply = self.coinmarketcap.conv(conv_value, conv_from, conv_to)
			except Exception as e:
				print("DEBUG: %s" % (e))
		except Exception as e:
			print("DEBUG: %s" % (e))
		return reply

	def list(self):
		available_to = ' '.join(coinmarketcap_valid.converts)
		available_from = list()
		for c in coinmarketcap_valid.cryptos:
			available_from.append(c)
		return'Available <from> currencies: %s\n\nAvailable <to> currencies: %s' % (' '.join(available_from), available_to)

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

