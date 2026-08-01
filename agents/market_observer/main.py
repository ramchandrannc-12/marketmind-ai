import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

#symbol = "RELIANCE"
#instrument_key = "NSE_EQ|INE002A01018"
#api_symbol = f"NSE_EQ:{symbol}"
watchlist = [
    {
        "symbol": "RELIANCE",
        "instrument_key": "NSE_EQ|INE002A01018"
    },
    {
        "symbol": "TCS",
        "instrument_key": "NSE_EQ|INE467B01029"
    }
]
stock = watchlist[0]

symbol = stock["symbol"]
instrument_key = stock["instrument_key"]
api_symbol = f"NSE_EQ:{symbol}"
access_token = os.getenv("UPSTOX_ACCESS_TOKEN")

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
    "instrument_key": instrument_key
}

response = requests.get(url, headers=headers, params=params)

print("Upstox API Status:", response.status_code)
print(response.json())
data = response.json()

reliance_data = data["data"][api_symbol]

real_price = reliance_data["last_price"]
real_previous_close = reliance_data["cp"]
real_volume = reliance_data["volume"]
last_trade_quantity = reliance_data["ltq"]

print(f"REAL {symbol} DATA")
print("Current Price:", real_price)
print("Previous Close:", real_previous_close)
print("Volume:", real_volume)
print("Last Trade Quantity:", last_trade_quantity)
real_price_change = (
    (real_price - real_previous_close) / real_previous_close
) * 100

print("Real Price Change:", round(real_price_change, 2), "%")

if real_price_change >= 1:
   print(f"LIVE ALERT: {symbol} moved UP by 1% or more")

elif real_price_change <= -1:
    print(f"LIVE ALERT: {symbol} moved DOWN by 1% or more")

else:
    print("LIVE: No significant price movement")

to_date = datetime.today().strftime("%Y-%m-%d")
from_date = (datetime.today() - timedelta(days=10)).strftime("%Y-%m-%d")

historical_url = (
    f"https://api.upstox.com/v3/historical-candle/"
    f"{instrument_key}/days/1/{to_date}/{from_date}"
)

historical_response = requests.get(
    historical_url,
    headers=headers
)

print("\nHistorical API Status:", historical_response.status_code)
historical_data = historical_response.json()

candles = historical_data["data"]["candles"]

historical_changes = []

print("\nNumber of candles:", len(candles))

print("\nFirst Candle:")
print(candles[0])
total_volume = 0

for candle in candles:
    total_volume = total_volume + candle[5]

for candle in candles:

    open_price = candle[1]
    close_price = candle[4]

    change = ((close_price - open_price) / open_price) * 100

    historical_changes.append(round(change, 2))

print("\nTotal Historical Volume:", total_volume)
average_volume = total_volume / len(candles)
print("Average Historical Volume:", average_volume)

print("\nHistorical Daily Changes:")

for change in historical_changes:
    print(change, "%")
print("\nSIMILAR DAYS")

similar_days = 0
next_day_up = 0
next_day_down = 0

print("\nSIMILAR DAYS")

for i in range(len(historical_changes) - 1):

    current_change = historical_changes[i]

    if abs(current_change - real_price_change) <= 0.25:

        print(f"Similar Day: {current_change}%")

        similar_days += 1

        next_day_change = historical_changes[i + 1]

        if next_day_change > 0:
            next_day_up += 1
        else:
            next_day_down += 1

print(f"\nTotal Similar Days: {similar_days}")

print("\nPREDICTION ENGINE")

print(f"Next Day Up   : {next_day_up}")
print(f"Next Day Down : {next_day_down}")

if similar_days > 0:

    probability = (next_day_up / similar_days) * 100

    print(f"Bullish Probability : {round(probability,1)}%")

    print(f"Historical Matches : {similar_days}")

    if similar_days >= 20:
        print("Prediction Confidence : 🟢 High")

    elif similar_days >= 10:
        print("Prediction Confidence : 🟡 Medium")

    else:
        print("Prediction Confidence : 🔴 Low")

else:
    print("Not enough historical matches.")

live_volume = data["data"][api_symbol]["volume"]

volume_ratio = live_volume / average_volume

print("\nLive Volume:", live_volume)
print("Average Volume:", round(average_volume))
print("Volume Ratio:", round(volume_ratio, 2))
if volume_ratio >= 3:
    print("🔴 EXTREME Volume Spike")

elif volume_ratio >= 2:
    print("🟠 HIGH Volume Spike")

elif volume_ratio >= 1.5:
    print("🟡 MODERATE Volume Spike")

else:
    print("🟢 NORMAL Volume")

print("\nMARKET INSIGHT")

if real_price_change >= 1 and volume_ratio >= 1.5:
    print("🟢 Strong Bullish Momentum")

elif real_price_change <= -1 and volume_ratio >= 1.5:
    print("🔴 Strong Bearish Momentum")

elif real_price_change >= 1 and volume_ratio < 1.5:
    print("🟡 Weak Breakout (Low Volume)")

elif real_price_change <= -1 and volume_ratio < 1.5:
    print("🟠 Weak Selling Pressure")

else:
    print("⚪ No significant momentum")

print("\nAI EXPLANATION")

if real_price_change >= 1 and volume_ratio >= 1.5:
    print(f"Price increased by {round(real_price_change,2)}%.")
    print(f"Volume is {round(volume_ratio,2)}x the historical average.")
    print("This indicates strong buying interest.")

elif real_price_change <= -1 and volume_ratio >= 1.5:
    print(f"Price decreased by {round(abs(real_price_change),2)}%.")
    print(f"Volume is {round(volume_ratio,2)}x the historical average.")
    print("This indicates strong selling pressure.")

elif real_price_change >= 1 and volume_ratio < 1.5:
    print(f"Price increased by {round(real_price_change,2)}%.")
    print(f"Volume is only {round(volume_ratio,2)}x the historical average.")
    print("The breakout lacks strong volume confirmation.")

elif real_price_change <= -1 and volume_ratio < 1.5:
    print(f"Price decreased by {round(abs(real_price_change),2)}%.")
    print(f"Volume is below the historical average ({round(volume_ratio,2)}x).")
    print("Selling pressure appears weak.")

else:
    print("No meaningful price or volume signal was detected.")

print("\nCONFIDENCE SCORE")

confidence = 50

print("Base Confidence : 50 (Neutral Starting Point)")

# Price Strength
if abs(real_price_change) >= 2:
    confidence += 20
    print("+20 : Strong Price Movement (>=2%)")

elif abs(real_price_change) >= 1:
    confidence += 10
    print("+10 : Moderate Price Movement (>=1%)")

else:
    print("+0  : Weak Price Movement")

# Volume Strength
if volume_ratio >= 3:
    confidence += 30
    print("+30 : Extreme Volume")

elif volume_ratio >= 2:
    confidence += 20
    print("+20 : High Volume")

elif volume_ratio >= 1.5:
    confidence += 10
    print("+10 : Moderate Volume")

else:
    print("+0  : Normal/Low Volume")

print("---------------------------")
print(f"Confidence Score : {confidence}/100")

if confidence >= 80:
    print("🟢 High Confidence")

elif confidence >= 60:
    print("🟡 Medium Confidence")

else:
    print("🔴 Low Confidence")