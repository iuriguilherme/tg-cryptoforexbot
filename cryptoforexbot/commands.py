# vim:fileencoding=utf-8

from plugins.coinmarketcap.wrapper import coinmarketcap
from plugins.coinmarketcap import valid as coinmarketcap_valid
from plugins.log.stdout import stdout as log

class commands():

	def __init__(self):
		self.log = log()

	def command_conv(self, command):
		self.log.cmd(' '.join(command))
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
				self.log.err("%s" % (e))
		except Exception as e:
			self.log.err("%s" % (e))
		return reply

	def command_list(self, command):
		self.log.cmd(' '.join(command))
		available_to = ' '.join(coinmarketcap_valid.converts)
		available_from = list()
		for c in coinmarketcap_valid.cryptos:
			available_from.append(c)
		return'Available <from> currencies: %s\n\nAvailable <to> currencies: %s' % (' '.join(available_from), available_to)

	def command_price(self, command):
		self.log.cmd(' '.join(command))
		reply = texts.err_param[2]
		string_pattern = re.compile('\w+')
		##TODO: When things go wrong, we want to know whether it's the API fault or a code screw up
		try:
			crypto = str(''.join(re.findall(string_pattern, command[1])))
			reply = texts.err_param[0]
			try:
				reply = self.coinmarketcap.price(crypto)
			except Exception as e:
				self.log.err("%s" % (e))
		except Exception as e:
			self.log.err("%s" % (e))
		return reply

