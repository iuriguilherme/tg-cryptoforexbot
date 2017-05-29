# vim:fileencoding=utf-8
## Coinmarketcap API documented at https://coinmarketcap.com/api/
## Requests documentation at http://docs.python-requests.org/en/latest

import requests
from cryptoforexbot import metadata, texts

class v1():
  def __init__(self):
    self.api_url = 'https://api.coinmarketcap.com/v1/'
    self.agent = str('/'.join([metadata.agent, metadata.version]))
    self.headers = {'user-agent': self.agent}

  def __get(self, url, params={'':''}):
    ## TODO: sanitize url
    safe_url = url
    request_url = ''.join([self.api_url, safe_url])
    try:
      response = requests.get(request_url, headers=self.headers, params=params)
    except Exception as e:
      return (False, texts.err_api[1], texts.err_api[1])
    if response.status_code == requests.codes.ok:
      return (True, response.json(), response.json())
    else:
      return (False, texts.err_api[0], texts.err_api[0])
    return (False, False, 'DEBUG %s%srequest_url: %s' % (self, '\n', request_url))

  def get_ticker(self, limit=0, convert=''):
    ## TODO: sanitize params
    safe_limit = limit
    safe_convert = convert
    url = 'ticker/'
    params = {'limit' : safe_limit, 'convert': safe_convert}
    return self.__get(url, params)

  def get_ticker_id(self, currency='bitcoin', convert=''):
    ## TODO: sanitize params
    safe_currency = currency
    safe_convert = convert
    url = ''.join(['ticker/', safe_currency, '/'])
    params = {'convert': safe_convert}
    return self.__get(url, params)

  def get_global(self, convert):
    ## TODO: sanitize params
    safe_convert = convert
    url = 'global/'
    params = {'convert': safe_convert}
    return self.__get(url, params)

