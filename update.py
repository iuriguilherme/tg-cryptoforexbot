#!/usr/bin/python
## This makes the coin information available at https://api.coinmarketcap.com/v1/ticker as a json file like https://github.com/desci/tg-cryptoforexbot/blob/master/plugins/coinmarketcap/cryptos.json

import json
from plugins.coinmarketcap.api import v1 as api

class update_coinmarketcap():
	def __init__(self):
		self.api = api()
		self.coinmarketcap()
	def coinmarketcap(self):
		cryptos_file = 'plugins/coinmarketcap/cryptos.json'
		ticker = self.api.get_ticker()
		cryptos = json.load(open(cryptos_file))

		for coin in ticker:
			if not cryptos.has_key(coin["symbol"]):
				cryptos.update({coin["symbol"]:{"name":coin["name"],"coinmarketcap_id":coin["id"],"symbols":[coin["id"],coin["symbol"]]}})

		json.dump(cryptos, open(cryptos_file, 'w'), indent=True, sort_keys=True, ensure_ascii=False)

if __name__ == "__main__":
	update_coinmarketcap = update_coinmarketcap()

