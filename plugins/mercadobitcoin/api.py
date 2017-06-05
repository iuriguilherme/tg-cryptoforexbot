# vim:fileencoding=utf-8
## Mercado Bitcoin API documented at https://www.mercadobitcoin.com.br/api-doc/
## Requests documentation at http://docs.python-requests.org/en/latest

import requests
from cryptoforexbot import metadata, texts

class v2():
  def __init__(self):
    self.api_url = 'https://www.mercadobitcoin.net/api/'
    self.agent = str('/'.join([metadata.agent, metadata.version]))
    self.headers = {'user-agent': self.agent}

  def __get(self, url, params={'':''}):
    ## TODO: sanitize url
    safe_url = url
    request_url = ''.join([self.api_url, safe_url])
    try:
      response = requests.get(request_url, headers=self.headers, params=params)
    except Exception as e:
      return (False, texts.err_api[3], 'DEBUG %s%sexception: %s' % (self, '\n', e))
    if response.status_code == requests.codes.ok:
      return (True, response.json(), response.json())
    else:
      return (False, texts.err_api[2], 'DEBUG %s%sresponse: %s' % (self, '\n', response))
    return (False, False, 'DEBUG %s%srequest_url: %s' % (self, '\n', request_url))

  def get_ticker(self, version='v2', litecoin='litecoin'):
    ## TODO: sanitize params
    safe_version = version
    base_url = 'ticker'
    if litecoin:
      base_url = '_'.join([base_url, 'litecoin'])
    url = '/'.join([version, base_url, ''])
    #url = '%s/%s' % (version, base_url)
    params = {}
    return self.__get(url, params)

  def get_orderbook(self, litecoin='litecoin'):
    ## TODO: sanitize params
    base_url = 'orderbook'
    if litecoin == 'litecoin':
      base_url = '_'.join([base_url, 'litecoin'])
    url = '/'.join([base_url, ''])
    params = {}
    return self.__get(url, params)

  def get_trades(self, litecoin='litecoin'):
    ## TODO: sanitize params
    base_url = 'trades'
    if litecoin == 'litecoin':
      base_url = '_'.join([base_url, 'litecoin'])
    url = '/'.join([base_url, ''])
    params = {}
    return self.__get(url, params)

  def get_trades_param(self, tid=False, since=False, timestamp_inicial=False, timestamp_final=False, litecoin='litecoin'):
    ## TODO: sanitize params
    base_url = 'trades'
    if litecoin == 'litecoin':
      base_url = '_'.join([base_url, 'litecoin'])
    url = '/'.join([base_url, ''])
    params = {}
    if timestamp_inicial:
      if timpestamp_final:
        base_url = '/'.join([timestamp_inicial, timestamp_final, base_url])
      else:
        base_url = '/'.join([timestamp_inicial, base_url])
    if tid:
      params = {'tid': tid}
    elif since:
      params = {'since': since}
    return self.__get(url, params)

