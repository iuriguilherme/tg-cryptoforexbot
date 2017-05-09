Crypto Forex Bot for Telegram
===

What
---

This is a [Python](https://python.org) [Telegram bot](https://telegram.org/faq#bots) to convert values between [crypto](https://en.wikipedia.org/wiki/Criptocurrency) and fiat currencies.  
It is currently pre-alpha and does not do anything.  
The intended implementation resides at [@criptoforexbot](https://telegram.me/cryptoforexbot).  

Usage
---

You can use the bot [@criptoforexbot](https://telegram.me/cryptoforexbot) on [Telegram](https://telegram.org).  
If you want to make your own, then first get a token from [@BotFather](https://telegram.me/botfather).  
Then install the dependencies:  

### Dependencies

This has been tested with Python 2.7  
If you don't have Python, [install it!](https://www.python.org/downloads/)  

We use [Telepot](https://github.com/nickoala/telepot), so you have to install it.  
Try `pip install telepot`. Or you can try `pip install -r requirements.txt` from *cryptoforexbot*'s directory.  

### Configuring

Enter the directory *cryptoforexbot*.  
Rename the file `cryptoforexbot.cfg.example` to `cryptoforexbot.cfg`.  
Edit that file, changing the value `token` to the one [@BotFather](https://telegram.me/botfather) told you.  

### Running

Go back to the top directory.  
If on UNIX, run with `./start.py`  
On any platform, run with `python start.py`  
To stop, send a *KeyboardInterrupt* (CTRL+C).  

License
---

Copyleft 2017 Desobediente Civil

This is GPL software. Which basically means that if you modify the source code, you need to distribute the modified version WITH the modified source code and with the same license.  
See the file LICENSE which should be distributed with this software.  

