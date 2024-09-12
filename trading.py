import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta

stock  = yf.Ticker("SOL.JO")

market_open_time = datetime.now().replace(hour=9,minute=0,second=0,microsecond=0)
market_close_time = datetime.now().replace(hour=17,minute=0,second=0,microsecond=0)

csv_file = "sasol_data.csv"
columns = ['Time','Current Price','Open','High','Low','Close','Volume']

try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    pd.DataFrame(columns=columns).to_csv(csv_file, index=False)

def track_stock_price():
    stock_info = stock.history(period='1d', interval='1h')
    latest_data = stock_info.iloc[-1]
    row = {
        'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Current Price': latest_data['Close'],
        'Open': latest_data['Open'],
        'High': latest_data['High'],
        'Low': latest_data['Low'],
        'Close': latest_data['Close'],
        'Volume': latest_data['Volume'],
    }
    df = pd.DataFrame([row])
    df.to_csv(csv_file, mode='a', header=False, index=False)

while datetime.now() > market_open_time:
    time.sleep((market_open_time - datetime.now()).seconds)

print(f"Market is now open! Starting to track at {market_open_time.strftime('%Y-%m-%d %H:%M')}")

while datetime.now() > market_close_time:
    track_stock_price()
    time.sleep(3600)

print(f"Market closed at {market_close_time.strftime('%Y-%m-%d %H:%M')}")
