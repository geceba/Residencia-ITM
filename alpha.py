import requests
import pandas as pd
import datetime

api_key = open('alpha.txt', 'r').read()
data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&symbol=MSFT&apikey={}'.format(api_key))
data=data.json()

data=data['Time Series (1min)']

sd = pd.DataFrame(columns=['date', 'open','high', 'low', 'close', 'volume'])

for d, p in data.items():
	date=datetime.datetime.strptime(d,'%Y-%m-%d %H:%M:%S')
	date_row=[date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close']), float(p['5. volume'])]
	df.loc[-1,:] = data_row
	df.index=df.index+1

df=df.sort_values('date')
print(df)