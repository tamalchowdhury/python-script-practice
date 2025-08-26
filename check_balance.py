import os
import logging
import requests
from typing import Optional


try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


logging.basicConfig(level=logging.INFO)


class NotificationError(Exception):
    pass


def fetch_data(account_no: str) -> Optional[float]:
    URL = "https://prepaid.desco.org.bd/api/unified/customer/getBalance"
    params = {'accountNo': account_no}
    try:
        res = requests.get(
            url=URL,
            params=params,
            verify=False,
            timeout=10)
        res.raise_for_status()
        data = res.json()
        inner_data = data.get("data")
        return inner_data.get("balance") if inner_data else None
    except requests.RequestException as err:
        logging.error(f"Could not fetch, {err}")
        return None


def telegram_notify(balance: float, token: str, chat_id: str) -> tuple[bool, str]:
    if not token or not chat_id:
        return False, "Telegram not configured"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        res = requests.post(url, json={
            "chat_id": chat_id, "text": f"The current desco balance is {balance}"}, timeout=20)
        res.raise_for_status()
        return True, "Telegram sent"
    except requests.RequestException as e:
        return False, f"Telegram failed: {e}"


def send_notification(balance: float):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    success, msg = telegram_notify(balance, token, chat_id)
    logging.info(msg)

    if not success:
        raise NotificationError(msg)


def main():
    account_no = os.environ.get("ACCOUNT_NO")
    if not account_no:
        logging.error("ACCOUNT_NO not set")
        return
    balance = fetch_data(account_no)
    if balance is not None:
        msg = f"Current balance is {balance}"
        logging.info(msg)
        send_notification(balance)


if __name__ == "__main__":
    main()
