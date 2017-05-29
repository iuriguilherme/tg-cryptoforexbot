#!/usr/bin/env python
# vim:fileencoding=utf-8
## This is the main script and where cryptoforexbot should be started.
## If `./start.py` doesn't work for you, try `python start.py`.

## Python3
#try:
#  import asyncio
#  import telepot.aio
#except ImportError:
#  pass

from cryptoforexbot.bot import cryptoforex as cryptoforexbot

if __name__ == "__main__":
  cryptoforexbot()

