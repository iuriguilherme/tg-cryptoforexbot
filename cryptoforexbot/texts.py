# vim:fileencoding=utf-8

from cryptoforexbot import metadata

## Commands
help = """
Crypto Forex Bot help

This bot convert values in some cryptocurrencies to fiat currencies.

To see the price info for a cryptocurrency, use /price%s <coin>
Example: /price%s ETH

To convert values, use /conv%s <value> <from> <to>
Where <value> must be a valid float (commas will be ignored);
<from> may be a coinmarketcap id or a cryptocurrency symbol;
<to> may be USD or other available fiat currency;

Example: /conv%s 1,000.000 BTC USD

To see a list of available currencies, type /list%s
""" % (metadata.handle, metadata.handle, metadata.handle, metadata.handle, metadata.handle)
info = """
Crypto Forex Bot information

The source code for this bot resides on github: https://github.com/desci/tg-cryptoforexbot

The purpose of this bot is to convert values between cryptocurrencies as well as fiat currencies.

The current state of development is `alpha`.

There is a channel if you are interested in helping / following the development: https://t.me/joinchat/AAAAAA5gJhDL8TwBpxo5yw
"""
admin = """
Crypto Forex Bot admin instructions

Implemented options

/send - Send message to a group or user
Parameters: <id> <message>
Example: /send 0 This bot has been hacked

Unimplemented options

/dbadd - Adds a new coin to the database.
Parameters: <SYMBOL> <ISO 4217 SYMBOL> <Name> <current SDR value> <current BTC value> <API update link ('' for none)>
Example: /dbadd BTC XBT Bitcoin 1000 1 'bitcoin'

/dbdel - Removes a coin from the database
Parameters: <SYMBOL>
Example: /dbdel BTC

/dbedit - Edit a coin in the database
Parameters: <SYMBOL> <row> <value>
Example: /dbedit BTC sdr 1100
<row> can be one of: symbol, isosymbol, name, sdr, btc, api

/dblist - Show current coin values
Parameters: <SYMBOL>
Example: /dblist BTC

/dbupdate - Update SRD or BTC value with API if present

Regular user and group options should be available.

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

err_param = [
# 0
"""
I'm sorry, something happened and I couldn't proccess this request.
The admin has been notified. I think.
""",
# 1
"""
Incorrect parameters. Usage: /conv%s <value> <from> <to>

Example: /conv%s 1,000.000 BTC USD

For a list of available currencies, try /list%s
""" % (metadata.handle, metadata.handle, metadata.handle),
# 2
"""
Incorrect parameters. Usage: /price%s <coin>

Example: /price%s BTC

For a list of available currencies, try /list%s
""" % (metadata.handle, metadata.handle, metadata.handle),
# 3
"""
Incorrect parameters. Usage: /send%s <to> <message>
Where <to> is a telegram id.

Example: /send%s 0 This bot has been hacked
""" % (metadata.handle, metadata.handle),
# 4
"Not implemented."
]

err_valid = """
You've sent an unsupported or inexistent currency.

To see all available currencies, try /list%s
""" % (metadata.handle)

err_group = [
"This command is only available as a private message. Click on %s to message me." % (metadata.handle)
]

