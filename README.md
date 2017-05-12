Crypto Forex Bot for Telegram
===

What
---

This is a [Python](https://python.org) [Telegram bot](https://telegram.org/faq#bots) to convert values between [crypto](https://en.wikipedia.org/wiki/Criptocurrency) and [fiat](https://en.wikipedia.org/wiki/Fiat_money) currencies.  
The intended implementation resides at [@criptoforexbot](https://telegram.me/cryptoforexbot).  

Usage
---

You can use the bot [@criptoforexbot](https://telegram.me/cryptoforexbot) on [Telegram](https://telegram.org).  

There is a telegram group if you are interested in following or helping the development: <https://t.me/joinchat/AAAAAA5gJhDL8TwBpxo5yw> **disable notifications, this group gets a LOT of messages**  

### Commands

Currently available commands:

#### /help

Display a (helpfully) helpful information, as a guide for usage;

#### /info

Display information about the bot, link to the source code and the development group;

#### /conv

Convert values from one currency to another.

Example: `/conv 0.003 BTC BRL`

#### /price

Display price information for a currency.

Example: `/price ETH`

#### /list

Lists current available currencies that can be used with the other commands.

#### /feedback

Send feedback to the development team.

Example: `/feedback This bot doesn't work!`

---

Make your own
---

If you want to make your own bot based on this one, then:  

### Register as a Telegram Bot

First get a token from [@BotFather](https://telegram.me/botfather) on Telegram. See the [bot faq](https://telegram.org/faq#bots) for reference.  

### Get the working code

Do not just clone the main branch. I commit everything. Use the [*stable* release tag](https://github.com/desci/tg-cryptoforexbot/releases/tag/stable):  

```bash
$ git clone https://github.com/desci/tg-cryptoforexbot.git
$ cd tg-cryptoforexbot
$ git checkout stable
```

### Dependencies

This has been tested with Python 2.7.11  
If you don't have Python, [install it!](https://www.python.org/downloads/)  

We use [Telepot](https://github.com/nickoala/telepot), so you have to install it.  
Try `pip install telepot`. Or you can try `pip install -r requirements.txt` from *cryptoforexbot*'s directory.  

### Configuring

Enter the directory *cryptoforexbot*.  
Rename the file `cryptoforexbot.cfg.example` to `cryptoforexbot.cfg`.  
Edit that file, changing the value `token` in the `[botfather]` section to the one [@BotFather](https://telegram.me/botfather) told you.  

### Running

Go back to the top directory.  
If on UNIX, run with `./start.py`  
On any platform, run with `python start.py`  
To stop, send a *KeyboardInterrupt* (CTRL+C).  

### Admin

If you don't know what is your telegram id, make sure you leave the debugging logs on and send a private message to your bot.  
You should see something like this:  

    [2017-05-09 13:37:26.113188] RCV: Received "hi" from 123456789

Where `123456789` is your telegram id. Make sure you put that in the configuration file, in the `[admin]` section - the file is `cryptoforexbot/cryptoforexbot.cfg` as explained above, see **Configuring**.  

Also, you may configure a group admin id, which looks like `-123456789`. This will help with debug logging and it's where the user feedback is sent.

#### Admin commands

The following additional admin commands are available:

##### /admin

Like `/help`, but for admin commands.

~~When the bot is successfully acknowledging you as an admin, send the `/admin` command to get help on how to manage the database.~~  

~~Using a local database to store values is important because querying external APIs everytime an user make a request would overhead the APIs, also they could be temporary unreachable because of network lag.~~  

*database not yet implemented, see roadmap below*

##### /send

Send a message (from the bot) to any telegram user or group.

Usage: `/send <id> <message>`

##### /debug

Command which can be used for debbuging purposes, defined at `cryptoforexbot/admin_commands.py` and freely hackable.

### Systemd

If you are running the bot on a Linux server (or other systemd capable), use the following *systemd* service file for a daemon:

```systemd
[Unit]
Description=tg-cryptoforexbot daemon
After=network.target nss-lookup.target

[Service]
Type=simple
ExecStart=/usr/bin/python2.7 /home/user/tg-cryptoforexbot/start.py
WorkingDirectory=/home/user/tg-cryptoforexbot/
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

On a Debian system, this should reside at `/lib/systemd/system/tg-cryptoforexbot.service`.

Enable the service and start:

```bash
# systemctl daemon-reload
# systemctl enable tg-cryptoforexbot.service
# systemctl -l start tg-cryptoforexbot.service
```

To see if it's working:

```bash
# systemctl -l status tg-cryptoforexbot.service
```

To stop:

```bash
# systemctl stop tg-cryptoforexbot.service
```

Or restart:

```bash
# systemctl -l restart tg-cryptoforexbot.service
```

#### Crontab

You can also put a watchdog cronjob to make sure it will restart on failure:

```bash
# crontab -e
```

Add a line like this in the crontab:

```crontab
*/10 * * * * /usr/lib/systemctl is-active tg-cryptoforexbot.service || /usr/lib/systemctl start tg-cryptoforexbot.service
```

This would check every 10 minutes if the bot is running and start it in case it wasn't.

Roadmap
---

### TODO

- [ ] Add as many currencies as possible;

- [ ] Use as many external websites API as possible, in case some of them gets rate limit or suffer downtime;

- [ ] Use sqlite or other database to store coin information and values;

- [ ] Use inline commmands;

- [ ] Translations;

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
See the file *LICENSE.md* which should be distributed with this software.  

### Assets

Logo found in subdirectory *assets/* uses the [orange bitcoin symbol](https://en.bitcoin.it/wiki/Promotional_graphics) which is available in the public domain, as well as an edited graphic chart image obtained from <http://www.netpicks.com/forex-trading-2/forex-trading-charts/>. Both the scalable vector and the exported PNG image are licensed under CC0. See the file *ASSETS-LICENSE.txt*.

