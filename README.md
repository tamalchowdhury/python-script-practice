# DESCO Balance Bot Script

## Setting up Locally:

- You need `Python 3` installed on your computer

Install the following Python dependencies:

```bash
pip install requests python-dotenv
```

Rename the `.env.sample` file to `.env` file:

```bash
mv .env.sample .env
```

## Setting up the Telegram bot:

1. Open Botfather https://t.me/botfather and follow the instructions to create your bot (e.g, Desco Balance Bot). You will get a telegram bot token. 
2. Copy and add it to `TELEGRAM_BOT_TOKEN` in the `.env` file.
3. Send a `hi/hello` chat to your new bot.
4. Open this URL in your browser `https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates`
5. Copy the chat `id` value and add it to the `TELEGRAM_CHAT_ID` in the `.env` file.

## Run the script:

```bash
python check_balance.py
```

Output:

```bash
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host 'prepaid.desco.org.bd'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(

(True, 'Telegram sent')
```

Ignore the SSL warning for now (I will update it later); you should see (True, 'Telegram sent`)

And receive a message in your Telegram app.

## Known issues:

It is possible that behind the scenes, DESCO is using multiple endpoints for quering various Meter types.

The endpoint this script is using is:

```text
https://prepaid.desco.org.bd/api/unified/customer/getBalance?accountNo=
```

So please test this endpoint with your DESCO account and first verify that this is working for your meter.