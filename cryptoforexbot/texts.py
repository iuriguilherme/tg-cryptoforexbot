# vim:fileencoding=utf-8

## Commands
help = """
Crypto Forex Bot

This bot does nothing at all.
As soon as development occurs, it will display prices and convert values for cryptocurrencies as well as fiat currencies.
Stay tuned.
"""
info = """
Crypto Forex Bot info

The source code for this bot resides on github: https://github.com/desci/tg-cryptoforexbot

The purpose of this bot is to convert cryptocurrencies as well as fiat currencies.
The current state of development is pre-alpha and so far, the bot does nothing at all.
You may follow the development at Github.
Or even help speed the development by either sending pull requests to the repository on Github, or money to @desci42 on Telegram
"""
info = """
Crypto Forex Bot admin instructions

*Note that none of these options have been implemented yet*

/add - Adds a new coin to the database.
Parameters: <SYMBOL> <ISO 4217 SYMBOL> <Name> <current SDR value> <current BTC value> <API update link ('' for none)>
Example: /add BTC XBT Bitcoin 1000 1 'bitcoin'

/del - Removes a coin from the database
Parameters: <SYMBOL>
Example: /del BTC

/edit - Edit a coin in the database
Parameters: <SYMBOL> <row> <value>
Example: /edit BTC sdr 1100
<row> can be one of: symbol, isosymbol, name, sdr, btc, api

/list - Show current coin values
Parameters: <SYMBOL>
Exampple: /list BTC

/update - Update SRD or BTC value with API if present

For cryptocurrencies, <API update link> is one of the "id" listed at https://api.coinmarketcap.com/v1/ticker

For fiat currencies, please refer to SDR's documentation: https://www.imf.org/external/np/fin/data/rms_sdrv.aspx
If you have a better idea than to use something other than SDR, let me know.

For currency symbols reference, see https://en.wikipedia.org/wiki/ISO_4217
"""

## Errors
err_config = """
Please rename cryptoforexbot.cfg.example to cryptoforexbot.cfg
and change the values to your own bot.
Talk to @BotFather on Telegram to obtain a token.
"""

