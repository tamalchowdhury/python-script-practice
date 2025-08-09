import requests

ACCOUNT_NO = "11488891"  # your DESCO account number
API_URL = f"https://prepaid.desco.org.bd/api/unified/customer/getBalance?accountNo={ACCOUNT_NO}"
URL = "https://prepaid.desco.org.bd/api/unified/customer/getBalance"


try:
    params = {'accountNo': ACCOUNT_NO}

    # TODO: fix the verify WARNING
    res = requests.get(url=URL, params=params, verify=False)
    if res.status_code == 200:
        print("Response was OK")
    data = res.json()

    inner_data = data.get("data")
    if inner_data is not None:
        balance = inner_data.get("balance")
        print(f"The current balance is {balance}")
    else:
        print("No balance data available")


except Exception as e:
    print(f"Run into an error {e}")
