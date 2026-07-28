import os
import requests
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("UPSTOX_ACCESS_TOKEN")

symbol = "RELIANCE"

print("Market Observer Agent starting...")
print("Symbol:", symbol)

if access_token:
    print("Upstox token loaded successfully.")
else:
    print("ERROR: Upstox token not found.")
url = "https://api.upstox.com/v3/market-quote/ltp"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

params = {
    "instrument_key": "NSE_EQ|INE002A01018"
}

response = requests.get(url, headers=headers, params=params)

print("Upstox API Status:", response.status_code)
print(response.json())
data = response.json()

reliance_data = data["data"]["NSE_EQ:RELIANCE"]

real_price = reliance_data["last_price"]
real_previous_close = reliance_data["cp"]
real_volume = reliance_data["volume"]
last_trade_quantity = reliance_data["ltq"]

print("REAL RELIANCE DATA")
print("Current Price:", real_price)
print("Previous Close:", real_previous_close)
print("Volume:", real_volume)
print("Last Trade Quantity:", last_trade_quantity)
real_price_change = (
    (real_price - real_previous_close) / real_previous_close
) * 100

print("Real Price Change:", round(real_price_change, 2), "%")

if real_price_change >= 1:
    print("LIVE ALERT: RELIANCE moved UP by 1% or more")

elif real_price_change <= -1:
    print("LIVE ALERT: RELIANCE moved DOWN by 1% or more")

else:
    print("LIVE: No significant price movement")