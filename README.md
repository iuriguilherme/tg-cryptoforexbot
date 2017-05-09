Crypto Forex Bot for Telegram
===

What
---

This is a [Python](https://python.org) [Telegram bot](https://telegram.org/faq#bots) to convert values between [crypto](https://en.wikipedia.org/wiki/Criptocurrency) and [fiat](https://en.wikipedia.org/wiki/Fiat_money) currencies.  
It is currently pre-alpha and does not do anything.  
The intended implementation resides at [@criptoforexbot](https://telegram.me/cryptoforexbot).  

Usage
---

You can use the bot [@criptoforexbot](https://telegram.me/cryptoforexbot) on [Telegram](https://telegram.org).  
If you want to make your own, then first get a token from [@BotFather](https://telegram.me/botfather).  
Then install the dependencies:  

### Dependencies

This has been tested with Python 2.7.11  
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

### Admin

If you don't know what is your telegram id, make sure you leave the debugging logs on and send a private message to your bot.  
You should see something like this:  

    [2017-05-09 13:37:26.113188] RCV: Received "hi" from 123456789

Where `123456789` is your telegram id. Make sure you put that in the configuration file (`cryptoforexbot.cfg` as explained above, see **Configuring**).  
Send `/admin` command to the bot to get help on how to manage the database.  

Using a local database to store values is important because querying external APIs everytime an user make a request would overhead the APIs, also they could be temporary unreachable because of network lag.

License
---

Copyleft 2017 Desobediente Civil  

This is GPL software. Which basically means that if you modify the source code, you need to distribute the modified version WITH the modified source code and with the same license.  
See the file LICENSE which should be distributed with this software.  

