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
When the bot is successfully acknowledging you as an admin, send the `/admin` command to get help on how to manage the database.  

Using a local database to store values is important because querying external APIs everytime an user make a request would overhead the APIs, also they could be temporary unreachable because of network lag.  

Disclaimer
---

This bot relies on external services, for instance on [Coin Market Cap](https://coinmarketcap.com) and [International Monetary Fund](https://imf.org) for current values fetching. This is so as to provide a convenient way to convert to the latest prices of currencies. However, I am **not** responsible for the accuratness of the values provided by those external services. In your ideal world, we would have only descentralized currencies directly manipulated by the market. Which is not our reality as of now.  

**This bot is provided in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Use at your own risk.**  

If you ever complain to me that you lost money because you saw a wrong value, I will laugh at you. That said, major finance websites that charges you lots of money annualy for "secure and trusted" market data use the **very same methods** that are being used here.  
So what they are charging for? They are charging you because they will be nice and won't say *"-we will laugh at you"* like I do. They would treat you as a customer, and not as an user like I do. So you're really paying to be pampered and feel special. Also they spend much money so they don't have one milisecond of downtime, and if they ever do, theorectically you may sue them.  
If you think this is useful and should stay online and available, consider donating.  

License
---

Copyleft 2017 Desobediente Civil  

This is GPL software. Which basically means that if you modify the source code, you need to distribute the modified version WITH the modified source code and with the same license.  
See the file LICENSE which should be distributed with this software.  

