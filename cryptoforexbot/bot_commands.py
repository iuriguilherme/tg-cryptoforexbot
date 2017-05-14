# vim:fileencoding=utf-8

import re
import json
import datetime

from cryptoforexbot import texts, metadata
from plugins.coinmarketcap.wrapper import coinmarketcap

class bot_commands():

	def __init__(self):
		self.coinmarketcap = coinmarketcap()

	def conv(self, conv_value, (from_type, (from_id, from_name)), (to_type, (to_id, to_name))):
		try:
			if from_type == 'crypto' and to_type == 'fiat':
				try:
					response = self.coinmarketcap.conv(from_id, to_id)
					if response[0]:
						result = float(float(conv_value) * float(response[2][0][''.join(['price_',to_id.lower()])]))
						return (True, True, ' '.join(["(from coinmarketcap.com):", '{:,.8f}'.format(float(conv_value)), from_name, "=" , ' '.join(['$', '{:,.2f}'.format(float(result)), to_name])]))
					elif response[1]:
						return (False, True, response[2])
					elif response[2]:
						return (False, False, response[2])
					else:
						return (False, True, texts.err_internal)
				except Exception as e:
					return (False, False, '%s' % (e))
				return (False, True, texts.err_internal)
			elif from_type == 'crypto' and to_type == 'crypto':
				try:
					try:
						response_from = self.coinmarketcap.conv(from_id, '')
						response_to = self.coinmarketcap.conv(to_id, '')
					except Exception as e:
						return (False, False, '%s' % (e))
					if response_from[0] and response_to[0]:
						try:
							result = float(float(float(float(float(conv_value) / 1.0) * float(response_from[2][0]['price_btc'])) / float(response_to[2][0]['price_btc']) ) * 1.0 )
						except Exception as e:
							return (False, False, '%s' % (e))
						try:
							return (True, True, ' '.join(["(from coinmarketcap.com):", '{:,.8f}'.format(float(conv_value)), from_name, "=" , '{:,.8f}'.format(float(result)), to_name]))
						except Exception as e:
							return (False, False, '%s' % (e))
					elif response_to[1]:
						return (False, True, response_to[2])
					elif response_to[2]:
						return (False, False, response_to[2])
					else:
						return (False, True, texts.err_internal)
				except Exception as e:
					return (False, False, '%s' % (e))
			elif from_type == 'fiat' and to_type == 'crypto':
				try:
					try:
						response = self.coinmarketcap.conv(to_id, from_id)
					except Exception as e:
						return (False, False, '%s' % (e))
					if response[0]:
						try:
							result = float(float(float(conv_value) * 1.0) / float(response[2][0][''.join(['price_',from_id.lower()])]))
						except Exception as e:
							return (False, False, '%s' % (e))
						try:
							return (True, True, ' '.join(["(from coinmarketcap.com):", ' '.join(['$', '{:,.2f}'.format(float(conv_value))]), from_name, "=" , '{:,.8f}'.format(float(result)), to_name]))
						except Exception as e:
							return (False, False, '%s' % (e))
					elif response_to[1]:
						return (False, True, response[2])
					elif response_to[2]:
						return (False, False, response[2])
					else:
						return (False, True, texts.err_internal)
				except Exception as e:
					return (False, False, '%s' % (e))
			elif from_type == 'fiat' and to_type == 'fiat':
				try:
					try:
						response_from = self.coinmarketcap.conv('bitcoin', from_id)
						response_to = self.coinmarketcap.conv('bitcoin', to_id)
					except Exception as e:
						return (False, False, '%s' % (e))
					if response_from[0] and response_to[0]:
						try:
							result = float(float(float(conv_value) * float(response_to[2][0][''.join(['price_',to_id.lower()])])) / float(response_from[2][0][''.join(['price_',from_id.lower()])]))
						except Exception as e:
							return (False, False, '%s' % (e))
						try:
							return (True, True, ' '.join(["(from coinmarketcap.com):", ' '.join(['$', '{:,.2f}'.format(float(conv_value))]), from_name, "=" , ' '.join(['$', '{:,.2f}'.format(float(result))]), to_name]))
						except Exception as e:
							return (False, False, '%s' % (e))
					elif response_to[1]:
						return (False, True, response_to[2])
					elif response_to[2]:
						return (False, False, response_to[2])
					else:
						return (False, True, texts.err_internal)
				except Exception as e:
					return (False, False, '%s' % (e))
			else:
				return (False, False, False)
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, True, texts.err_internal)

	def list(self):
		try:
			try:
				cryptos_dict = json.load(open('plugins/coinmarketcap/cryptos.json'))
				converts_dict = json.load(open('plugins/coinmarketcap/converts.json'))
			except Exception as e:
				return (False, True, '%s' % (e))

			reply_full = list()
			reply = list()
			reply.append("Aliases are case insensitive. Currently we only support currencies available at coinmarketcap.")
			reply.append('')
			reply.append('')

			reply_to = list()
			reply_to.append("Available fiat currencies:")
			reply_to.append('')

			reply_to_currencies = list()
			for convert in converts_dict:
				reply_to_currencies.append(''.join([converts_dict[convert]['name'], ' - aliases: ']))
				reply_to_currencies_symbols = list()
				for symbol in converts_dict[convert]['symbols']:
					reply_to_currencies_symbols.append(symbol)
				reply_to_currencies.append(''.join(['(', ', '.join(reply_to_currencies_symbols), ')']))
				reply_to_currencies.append('\n')
			reply_to.append(''.join(reply_to_currencies))

			reply.append('\n'.join(reply_to))
			reply.append('')

			reply_full.append('\n'.join(reply))

			reply_from = list()
			reply_from.append("Available cryptocurrencies:")
			reply_from.append('')

			reply_from_currencies = list()
			for crypto in cryptos_dict:
				reply_from_currencies.append(''.join([cryptos_dict[crypto]['name'], ' - aliases: ']))
				reply_from_currencies_symbols = list()
				for symbol in cryptos_dict[crypto]['symbols']:
					reply_from_currencies_symbols.append(symbol)
				reply_from_currencies.append(''.join(['(', ', '.join(reply_from_currencies_symbols), ')']))
				reply_from_currencies.append('\n')
				if len(''.join(reply_from_currencies)) > 3000:
					reply_full.append(''.join(reply_from_currencies))
					reply_from_currencies = list()
			reply_full.append('\n'.join([''.join(reply_from_currencies), 'END']))
			
			try:
				return (True, True, reply_full)
			except Exception as e:
				return (False, True, '%s' % (e))
		except Exception as e:
			return (False, True, '%s' % (e))
		return (False, False, False)

	def price(self, coin_id):
		try:
			response = self.coinmarketcap.price(coin_id)
			if response[0]:
				return (True, True, """
Price information for %s (from coinmarketcap.com)

Marketcap: U$$ %s

Price of 1 %s:
U$$ %s USD
%s BTC

Price change since last
hour: %s%%
day: %s%%
week: %s%%

Last 24 hours volume: U$$ %s

Available supply: %s %s
Total supply: %s %s

""" % (response[2][0]['name'], '{:,.2f}'.format(float(response[2][0]['market_cap_usd'])), response[2][0]['symbol'], '{:,.2f}'.format(float(response[2][0]['price_usd'])), '{:,.8f}'.format(float(response[2][0]['price_btc'])), response[2][0]['percent_change_1h'], response[2][0]['percent_change_24h'], response[2][0]['percent_change_7d'], '{:,.2f}'.format(float(response[2][0]['24h_volume_usd'])), '{:,.8f}'.format(float(response[2][0]['available_supply'])), response[2][0]['symbol'], '{:,.8f}'.format(float(response[2][0]['total_supply'])), response[2][0]['symbol']))
			elif response[1]:
				return (False, True, response[2])
			elif response[2]:
				return (False, False, response[2])
			else:
				return (False, True, texts.err_internal)
		except Exception as e:
			return (False, False, '%s' % (e))
		return (False, False, False)

	def debug(self, param):
		return (True, True, ' '.join(param))

