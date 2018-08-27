import requests
import csv
import pandas as pd


r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=TU10HCWDTV5CNVBN")

data = r.json()
print(type(data))

dicto = []

for valor in data["Time Series (Daily)"]:
	#print(data["Time Series (Daily)"][valor]["1. open"])
	d = data["Time Series (Daily)"][valor]
	dicto.append(d)

print(type(dicto))


df= pd.DataFrame(dicto)
print(df)
