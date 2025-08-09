import requests
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def fetch_data():
    ACCOUNT_NO = os.environ["ACCOUNT_NO"]
    URL = "https://prepaid.desco.org.bd/api/unified/customer/getBalance"
    params = {'accountNo': ACCOUNT_NO}

    try:
        res = requests.get(url=URL, params=params, verify=False)
        data = res.json()
        inner_data = data.get("data")
        if inner_data is not None:
            balance = inner_data.get("balance")
            return balance
        else:
            return None
    except Exception as err:
        print(f"Could not fetch, {err}")
        return None


def telegram_notify(balance):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False, "Telegram not configured (TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID)"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, json={
                          "chat_id": chat_id, "text": f"The current desco balance is {balance}"}, timeout=20)
        if r.ok:
            return True, "Telegram sent"
        return False, f"Telegram failed: HTTP {r.status_code} {r.text}"
    except Exception as e:
        return False, f"Telegram failed: {e}"


def send_notification(balance):
    res = telegram_notify(balance)
    print(res)


def main():
    # balance = fetch_data()
    balance = fetch_data()
    if balance is not None:
        send_notification(balance)


if __name__ == "__main__":
    main()
